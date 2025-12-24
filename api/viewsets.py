from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import HarvestJob, HarvestResult
from core.tasks import harvest_website

from .serializers import HarvestJobSerializer, HarvestResultSerializer


class HarvestJobViewSet(viewsets.ModelViewSet):
    queryset = HarvestJob.objects.all().order_by('-created_at')
    serializer_class = HarvestJobSerializer

    def perform_create(self, serializer):
        job = serializer.save()
        harvest_website.delay(str(job.id))

    @action(detail=True, methods=['get'])
    def result(self, request, pk=None):
        job = self.get_object()
        try:
            result = job.result
        except HarvestResult.DoesNotExist:
            return Response({'detail': 'Result not available yet.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = HarvestResultSerializer(result)
        return Response(serializer.data)


class HarvestResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HarvestResult.objects.select_related('job').order_by('-created_at')
    serializer_class = HarvestResultSerializer
