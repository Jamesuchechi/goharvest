from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import HarvestJobViewSet, HarvestResultViewSet
from .views import HarvestCreateView, TechDetectView

router = DefaultRouter()
router.register(r'jobs', HarvestJobViewSet, basename='jobs')
router.register(r'results', HarvestResultViewSet, basename='results')

urlpatterns = [
    path('', include(router.urls)),
    path('harvest/', HarvestCreateView.as_view(), name='harvest-create'),
    path('tech-detect/', TechDetectView.as_view(), name='tech-detect'),
]
