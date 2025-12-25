from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import (
    ComponentViewSet,
    HarvestJobViewSet,
    HarvestResultViewSet,
    TechnologyDetectionViewSet,
)

router = DefaultRouter()
router.register(r'jobs', HarvestJobViewSet, basename='jobs')
router.register(r'results', HarvestResultViewSet, basename='results')
router.register(r'tech-detect', TechnologyDetectionViewSet, basename='tech-detect')
router.register(r'components', ComponentViewSet, basename='components')

urlpatterns = [
    path('', include(router.urls)),
]
