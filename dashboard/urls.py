from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<uuid:job_id>/', views.job_detail, name='job_detail'),
]