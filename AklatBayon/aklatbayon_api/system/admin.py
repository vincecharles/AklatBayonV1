from django.contrib import admin
from .models import Setting, ActivityLog


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_type', 'model_id', 'created_at']
    list_filter = ['action', 'model_type']
    search_fields = ['description']
