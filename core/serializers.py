from rest_framework import serializers
from .models import HarvestJob, HarvestResult


class HarvestJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarvestJob
        fields = ['id', 'url', 'status', 'created_at', 'updated_at', 'options']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']


class HarvestResultSerializer(serializers.ModelSerializer):
    job = HarvestJobSerializer(read_only=True)

    class Meta:
        model = HarvestResult
        fields = ['job', 'content', 'html', 'assets', 'technologies', 'metadata', 'zip_file', 'created_at']
