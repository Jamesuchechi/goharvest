from rest_framework import serializers

from .models import (
    AIAnalysis,
    Asset,
    Component,
    HarvestJob,
    HarvestResult,
    HarvestSnapshot,
    PerformanceMetrics,
)


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = [
            'id',
            'url',
            'asset_type',
            'file_path',
            'file_size',
            'width',
            'height',
            'load_time',
            'is_critical',
            'is_lazy_loaded',
            'created_at',
        ]


class AIAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIAnalysis
        fields = [
            'id',
            'code_summary',
            'architecture_analysis',
            'component_list',
            'accessibility_score',
            'seo_score',
            'performance_score',
            'seo_suggestions',
            'accessibility_issues',
            'security_warnings',
            'tech_stack_summary',
            'similar_sites',
            'created_at',
        ]


class PerformanceMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceMetrics
        fields = [
            'id',
            'lighthouse_score',
            'performance_score',
            'accessibility_score',
            'best_practices_score',
            'seo_score',
            'largest_contentful_paint',
            'first_input_delay',
            'cumulative_layout_shift',
            'time_to_interactive',
            'total_blocking_time',
            'total_load_time',
            'dom_content_loaded',
            'first_contentful_paint',
            'total_requests',
            'total_transfer_size',
            'resource_breakdown',
            'created_at',
        ]


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = [
            'id',
            'component_type',
            'html',
            'css',
            'js',
            'name',
            'description',
            'screenshot',
            'usage_count',
            'is_bookmarked',
            'created_at',
        ]


class HarvestSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarvestSnapshot
        fields = [
            'id',
            'snapshot_date',
            'content_hash',
            'changes_detected',
            'diff_summary',
            'diff_details',
            'added_elements',
            'removed_elements',
            'modified_elements',
            'tech_changes',
        ]


class HarvestJobSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()

    class Meta:
        model = HarvestJob
        fields = [
            'id',
            'url',
            'user',
            'status',
            'created_at',
            'updated_at',
            'scheduled_at',
            'started_at',
            'completed_at',
            'options',
            'priority',
            'retry_count',
            'max_retries',
            'error_message',
            'tags',
            'notes',
            'estimated_duration',
            'is_recurring',
            'cron_schedule',
            'parent_job',
            'result',
        ]
        read_only_fields = [
            'id',
            'user',
            'status',
            'created_at',
            'updated_at',
            'started_at',
            'completed_at',
            'retry_count',
            'error_message',
            'result',
        ]

    def get_result(self, obj):
        if hasattr(obj, 'result'):
            return HarvestResultSerializer(obj.result, context=self.context).data
        return None


class HarvestJobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarvestJob
        fields = [
            'url',
            'options',
            'priority',
            'tags',
            'notes',
            'scheduled_at',
            'max_retries',
            'is_recurring',
            'cron_schedule',
        ]


class HarvestResultSerializer(serializers.ModelSerializer):
    job = HarvestJobSerializer(read_only=True)
    asset_details = AssetSerializer(many=True, read_only=True)
    ai_analysis = AIAnalysisSerializer(read_only=True)
    performance = PerformanceMetricsSerializer(read_only=True)
    components = ComponentSerializer(many=True, read_only=True)
    snapshots = HarvestSnapshotSerializer(many=True, read_only=True)

    class Meta:
        model = HarvestResult
        fields = [
            'id',
            'job',
            'content',
            'html',
            'structured_data',
            'assets',
            'total_assets',
            'total_size',
            'technologies',
            'frontend_framework',
            'css_framework',
            'metadata',
            'links',
            'zip_file',
            'json_export',
            'content_hash',
            'created_at',
            'asset_details',
            'ai_analysis',
            'performance',
            'components',
            'snapshots',
        ]
