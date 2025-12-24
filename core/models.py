from django.db import models
from django.contrib.auth.models import User
import uuid


class HarvestJob(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    options = models.JSONField(default=dict)  # e.g., {'mode': 'full', 'depth': 1}

    def __str__(self):
        return f"Harvest {self.url} - {self.status}"


class HarvestResult(models.Model):
    job = models.OneToOneField(HarvestJob, on_delete=models.CASCADE, related_name='result')
    content = models.TextField(blank=True)  # Extracted text
    html = models.TextField(blank=True)  # Full HTML
    assets = models.JSONField(default=list)  # List of asset URLs
    technologies = models.JSONField(default=dict)  # Detected tech stack
    metadata = models.JSONField(default=dict)  # Meta tags, etc.
    zip_file = models.FileField(upload_to='harvests/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.job}"