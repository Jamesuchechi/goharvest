from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'jobs', views.HarvestJobViewSet, basename='jobs')
router.register(r'results', views.HarvestResultViewSet, basename='results')
router.register(r'tech-detect', views.TechnologyDetectionViewSet, basename='tech-detect')
router.register(r'components', views.ComponentViewSet, basename='components')

urlpatterns = [
    path('', include(router.urls)),
]
