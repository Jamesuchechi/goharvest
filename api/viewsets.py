from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from core.models import Component, HarvestJob, HarvestResult
from core.tasks import harvest_website, schedule_recurring_harvest
from core.utils.compare import compare_results
from core.utils.reporting import generate_markdown_report
from core.utils.tech_detector import quick_tech_scan

from .serializers import (
    ComponentSerializer,
    HarvestJobCreateSerializer,
    HarvestJobSerializer,
    HarvestResultSerializer,
)


class HarvestJobViewSet(viewsets.ModelViewSet):
    queryset = HarvestJob.objects.all().select_related('result').order_by('-created_at')
    serializer_class = HarvestJobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return HarvestJobCreateSerializer
        return HarvestJobSerializer

    def perform_create(self, serializer):
        job = serializer.save(user=self.request.user)
        harvest_website.delay(str(job.id))

    @action(detail=True, methods=['get'])
    def result(self, request, pk=None):
        job = self.get_object()
        try:
            result = job.result
            serializer = HarvestResultSerializer(result)
            return Response(serializer.data)
        except HarvestResult.DoesNotExist:
            return Response(
                {'detail': 'Result not available yet.'},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=True, methods=['post'])
    def retry(self, request, pk=None):
        job = self.get_object()
        if job.status != 'failed':
            return Response(
                {'detail': 'Only failed jobs can be retried.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        job.status = 'pending'
        job.retry_count += 1
        job.error_message = ''
        job.save(update_fields=['status', 'retry_count', 'error_message'])

        harvest_website.delay(str(job.id))
        return Response({'detail': 'Job requeued for retry.'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        job = self.get_object()
        if job.status not in ['pending', 'running']:
            return Response(
                {'detail': 'Only pending/running jobs can be cancelled.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        job.status = 'cancelled'
        job.save(update_fields=['status'])
        return Response({'detail': 'Job cancelled.'})

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        job = self.get_object()
        try:
            result = job.result
            if not result.zip_file:
                return Response(
                    {'detail': 'ZIP file not available.'},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response({'download_url': result.zip_file.url})
        except HarvestResult.DoesNotExist:
            return Response(
                {'detail': 'Result not available yet.'},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=True, methods=['post'])
    def schedule(self, request, pk=None):
        job = self.get_object()
        cron_schedule = request.data.get('cron_schedule')

        if not cron_schedule:
            return Response(
                {'detail': 'cron_schedule is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        job.is_recurring = True
        job.cron_schedule = cron_schedule
        job.save(update_fields=['is_recurring', 'cron_schedule'])

        schedule_recurring_harvest.delay(str(job.id), cron_schedule)
        return Response({'detail': 'Recurring harvest scheduled.'})

    @action(detail=False, methods=['post'])
    def batch(self, request):
        urls = request.data.get('urls', [])
        options = request.data.get('options', {})

        if not urls:
            return Response(
                {'detail': 'urls list is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        jobs = []
        for url in urls:
            job = HarvestJob.objects.create(
                url=url,
                user=request.user,
                options=options,
            )
            jobs.append(job)
            harvest_website.delay(str(job.id))

        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        user = request.user
        total = HarvestJob.objects.filter(user=user).count()
        completed = HarvestJob.objects.filter(user=user, status='completed').count()
        failed = HarvestJob.objects.filter(user=user, status='failed').count()
        running = HarvestJob.objects.filter(user=user, status='running').count()

        return Response({
            'total_jobs': total,
            'completed': completed,
            'failed': failed,
            'running': running,
            'success_rate': (completed / total * 100) if total > 0 else 0,
        })


class HarvestResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HarvestResult.objects.select_related('job').order_by('-created_at')
    serializer_class = HarvestResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(job__user=self.request.user)

    @action(detail=True, methods=['get'])
    def export(self, request, pk=None):
        result = self.get_object()
        format_type = request.query_params.get('format', 'json')

        if format_type == 'json':
            if result.json_export:
                return Response({'download_url': result.json_export.url})
        elif format_type == 'markdown':
            markdown_content = generate_markdown_report(result)
            return Response({'markdown': markdown_content})

        return Response(
            {'detail': f'Format {format_type} not supported.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=False, methods=['get'])
    def search(self, request):
        tech = request.query_params.get('tech')
        if not tech:
            return Response(
                {'detail': 'tech parameter required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        results = self.get_queryset().filter(technologies__contains=tech)
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def compare(self, request, pk=None):
        result1 = self.get_object()
        result2_id = request.data.get('compare_with')

        if not result2_id:
            return Response(
                {'detail': 'compare_with ID required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result2 = get_object_or_404(HarvestResult, id=result2_id)
        comparison = compare_results(result1, result2)
        return Response(comparison)


class TechnologyDetectionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        url = request.data.get('url')
        if not url:
            return Response(
                {'detail': 'url is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        technologies = quick_tech_scan(url)
        return Response({'url': url, 'technologies': technologies})


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(result__job__user=self.request.user)

    @action(detail=True, methods=['post'])
    def bookmark(self, request, pk=None):
        component = self.get_object()
        component.is_bookmarked = not component.is_bookmarked
        component.save(update_fields=['is_bookmarked'])
        return Response({'bookmarked': component.is_bookmarked})
