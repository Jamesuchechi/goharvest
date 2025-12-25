from django.db import models
from django.contrib.auth.models import User
import uuid


class HarvestJob(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        (1, 'Urgent'),
        (5, 'Normal'),
        (10, 'Low'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    options = models.JSONField(default=dict)  # {'mode': 'full', 'depth': 2, 'extract_media': True}
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=5)
    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)
    error_message = models.TextField(blank=True)
    tags = models.JSONField(default=list)  # ['competitor-research', 'react']
    notes = models.TextField(blank=True)
    estimated_duration = models.DurationField(null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    cron_schedule = models.CharField(max_length=100, blank=True)  # '0 0 * * *'
    parent_job = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"Harvest {self.url} - {self.status}"


class HarvestResult(models.Model):
    job = models.OneToOneField(HarvestJob, on_delete=models.CASCADE, related_name='result')
    content = models.TextField(blank=True)
    html = models.TextField(blank=True)
    structured_data = models.JSONField(default=dict)
    assets = models.JSONField(default=list)
    total_assets = models.IntegerField(default=0)
    total_size = models.BigIntegerField(default=0)
    technologies = models.JSONField(default=dict)
    frontend_framework = models.CharField(max_length=50, blank=True)
    css_framework = models.CharField(max_length=50, blank=True)
    metadata = models.JSONField(default=dict)
    links = models.JSONField(default=dict)
    zip_file = models.FileField(upload_to='harvests/zips/', null=True, blank=True)
    json_export = models.FileField(upload_to='harvests/json/', null=True, blank=True)
    content_hash = models.CharField(max_length=64, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Result for {self.job.url}"


class Asset(models.Model):
    ASSET_TYPES = [
        ('image', 'Image'),
        ('css', 'CSS'),
        ('js', 'JavaScript'),
        ('font', 'Font'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]

    result = models.ForeignKey(HarvestResult, on_delete=models.CASCADE, related_name='asset_details')
    url = models.URLField()
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    file_path = models.FileField(upload_to='harvests/assets/')
    file_size = models.BigIntegerField()
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    load_time = models.FloatField(null=True, blank=True)
    is_critical = models.BooleanField(default=False)
    is_lazy_loaded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['asset_type', '-file_size']


class AIAnalysis(models.Model):
    result = models.OneToOneField(HarvestResult, on_delete=models.CASCADE, related_name='ai_analysis')
    code_summary = models.TextField()
    architecture_analysis = models.TextField()
    component_list = models.JSONField(default=list)
    accessibility_score = models.FloatField(null=True, blank=True)
    seo_score = models.FloatField(null=True, blank=True)
    performance_score = models.FloatField(null=True, blank=True)
    seo_suggestions = models.JSONField(default=list)
    accessibility_issues = models.JSONField(default=list)
    security_warnings = models.JSONField(default=list)
    tech_stack_summary = models.TextField()
    similar_sites = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Analysis for {self.result.job.url}"


class PerformanceMetrics(models.Model):
    result = models.OneToOneField(HarvestResult, on_delete=models.CASCADE, related_name='performance')
    lighthouse_score = models.JSONField(default=dict)
    performance_score = models.IntegerField(null=True)
    accessibility_score = models.IntegerField(null=True)
    best_practices_score = models.IntegerField(null=True)
    seo_score = models.IntegerField(null=True)
    largest_contentful_paint = models.FloatField(null=True)
    first_input_delay = models.FloatField(null=True)
    cumulative_layout_shift = models.FloatField(null=True)
    time_to_interactive = models.FloatField(null=True)
    total_blocking_time = models.FloatField(null=True)
    total_load_time = models.FloatField()
    dom_content_loaded = models.FloatField(null=True)
    first_contentful_paint = models.FloatField(null=True)
    total_requests = models.IntegerField(default=0)
    total_transfer_size = models.BigIntegerField(default=0)
    resource_breakdown = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)


class HarvestSnapshot(models.Model):
    original_result = models.ForeignKey(
        HarvestResult,
        on_delete=models.CASCADE,
        related_name='snapshots',
    )
    snapshot_date = models.DateTimeField(auto_now_add=True)
    content_hash = models.CharField(max_length=64)
    changes_detected = models.BooleanField(default=False)
    diff_summary = models.JSONField(default=dict)
    diff_details = models.TextField(blank=True)
    added_elements = models.JSONField(default=list)
    removed_elements = models.JSONField(default=list)
    modified_elements = models.JSONField(default=list)
    tech_changes = models.JSONField(default=dict)

    class Meta:
        ordering = ['-snapshot_date']


class RobotsCompliance(models.Model):
    domain = models.CharField(max_length=255, unique=True, db_index=True)
    robots_txt = models.TextField()
    last_checked = models.DateTimeField(auto_now=True)
    is_scrapable = models.BooleanField(default=True)
    crawl_delay = models.IntegerField(default=0)
    disallowed_paths = models.JSONField(default=list)

    def __str__(self):
        return f"Robots.txt for {self.domain}"


class HarvestAuditLog(models.Model):
    ACTION_CHOICES = [
        ('created', 'Job Created'),
        ('started', 'Job Started'),
        ('completed', 'Job Completed'),
        ('failed', 'Job Failed'),
        ('downloaded', 'Result Downloaded'),
        ('deleted', 'Job Deleted'),
    ]

    job = models.ForeignKey(HarvestJob, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user_ip = models.GenericIPAddressField()
    user_agent = models.TextField()
    details = models.JSONField(default=dict)

    class Meta:
        ordering = ['-timestamp']


class Component(models.Model):
    COMPONENT_TYPES = [
        ('button', 'Button'),
        ('card', 'Card'),
        ('navbar', 'Navigation Bar'),
        ('footer', 'Footer'),
        ('form', 'Form'),
        ('modal', 'Modal'),
        ('other', 'Other'),
    ]

    result = models.ForeignKey(HarvestResult, on_delete=models.CASCADE, related_name='components')
    component_type = models.CharField(max_length=50, choices=COMPONENT_TYPES)
    html = models.TextField()
    css = models.TextField(blank=True)
    js = models.TextField(blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    screenshot = models.ImageField(upload_to='components/screenshots/', null=True, blank=True)
    usage_count = models.IntegerField(default=1)
    is_bookmarked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-usage_count', '-created_at']
