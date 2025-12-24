from django.shortcuts import render
from core.models import HarvestJob


def index(request):
    jobs = HarvestJob.objects.all().order_by('-created_at')[:10]
    return render(request, 'dashboard/index.html', {'jobs': jobs})


def job_list(request):
    jobs = HarvestJob.objects.all().order_by('-created_at')
    return render(request, 'dashboard/job_list.html', {'jobs': jobs})


def job_detail(request, job_id):
    job = HarvestJob.objects.get(id=job_id)
    return render(request, 'dashboard/job_detail.html', {'job': job})