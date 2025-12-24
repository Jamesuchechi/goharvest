from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.tasks import harvest_website
from core.utils.robots_parser import RobotsParser
from core.utils.tech_detector import detect_technologies

from .serializers import HarvestJobSerializer


class HarvestCreateView(APIView):
    def post(self, request):
        serializer = HarvestJobSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        job = serializer.save()
        harvest_website.delay(str(job.id))
        return Response(HarvestJobSerializer(job).data, status=status.HTTP_201_CREATED)


class TechDetectView(APIView):
    def get(self, request):
        url = request.query_params.get('url')
        return self._handle(url)

    def post(self, request):
        url = request.data.get('url')
        return self._handle(url)

    def _handle(self, url):
        if not url:
            return Response({'detail': 'url is required.'}, status=status.HTTP_400_BAD_REQUEST)

        robots = RobotsParser()
        if not robots.can_fetch(url):
            return Response(
                {'detail': 'Robots.txt disallows scraping this URL'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        technologies = detect_technologies(url)
        return Response({'url': url, 'technologies': technologies})
