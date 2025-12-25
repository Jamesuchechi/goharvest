from django.contrib import admin
from .models import (
    AIAnalysis,
    Asset,
    Component,
    HarvestAuditLog,
    HarvestJob,
    HarvestResult,
    HarvestSnapshot,
    PerformanceMetrics,
    RobotsCompliance,
)


@admin.register(HarvestJob)
class HarvestJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'status', 'created_at', 'user')
    list_filter = ('status', 'created_at')
    search_fields = ('url',)


@admin.register(HarvestResult)
class HarvestResultAdmin(admin.ModelAdmin):
    list_display = ('job', 'created_at')
    search_fields = ('job__url',)


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('result', 'asset_type', 'file_size', 'created_at')
    list_filter = ('asset_type',)
    search_fields = ('url',)


@admin.register(AIAnalysis)
class AIAnalysisAdmin(admin.ModelAdmin):
    list_display = ('result', 'created_at')
    search_fields = ('result__job__url',)


@admin.register(PerformanceMetrics)
class PerformanceMetricsAdmin(admin.ModelAdmin):
    list_display = ('result', 'performance_score', 'accessibility_score', 'seo_score', 'created_at')
    search_fields = ('result__job__url',)


@admin.register(HarvestSnapshot)
class HarvestSnapshotAdmin(admin.ModelAdmin):
    list_display = ('original_result', 'changes_detected', 'snapshot_date')
    search_fields = ('original_result__job__url',)


@admin.register(RobotsCompliance)
class RobotsComplianceAdmin(admin.ModelAdmin):
    list_display = ('domain', 'is_scrapable', 'crawl_delay', 'last_checked')
    search_fields = ('domain',)


@admin.register(HarvestAuditLog)
class HarvestAuditLogAdmin(admin.ModelAdmin):
    list_display = ('job', 'action', 'timestamp', 'user')
    list_filter = ('action',)
    search_fields = ('job__url', 'user__username')


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'component_type', 'usage_count', 'is_bookmarked', 'created_at')
    list_filter = ('component_type', 'is_bookmarked')
    search_fields = ('name', 'description')
