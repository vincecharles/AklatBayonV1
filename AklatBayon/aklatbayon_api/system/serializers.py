from rest_framework import serializers
from .models import Setting, ActivityLog


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['id', 'key', 'value']


class ActivityLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True, default='System')

    class Meta:
        model = ActivityLog
        fields = ['id', 'user', 'username', 'action', 'description', 'model_type', 'model_id', 'ip_address', 'created_at']
        read_only_fields = ['user', 'ip_address', 'created_at']
