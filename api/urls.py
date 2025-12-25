from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .auth import MeView, RegisterView
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
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('auth/me/', MeView.as_view(), name='auth-me'),
    path('', include(router.urls)),
]
