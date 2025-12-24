from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import HarvestJob, HarvestResult
from .serializers import HarvestJobSerializer, HarvestResultSerializer
from .tasks import harvest_website


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
            serializer = HarvestResultSerializer(result)
            return Response(serializer.data)
        except HarvestResult.DoesNotExist:
            return Response({'detail': 'Result not available yet.'}, status=status.HTTP_404_NOT_FOUND)