from django.contrib import admin
from .models import HarvestJob, HarvestResult


@admin.register(HarvestJob)
class HarvestJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'status', 'created_at', 'user')
    list_filter = ('status', 'created_at')
    search_fields = ('url',)


@admin.register(HarvestResult)
class HarvestResultAdmin(admin.ModelAdmin):
    list_display = ('job', 'created_at')
    search_fields = ('job__url',)