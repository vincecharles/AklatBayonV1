from django.db import models
from django.conf import settings


class Setting(models.Model):
    """Key-value system settings."""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)

    def __str__(self):
        return f"{self.key} = {self.value}"


class ActivityLog(models.Model):
    """Audit log for tracking user actions."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='activity_logs'
    )
    action = models.CharField(max_length=100)  # e.g. 'created', 'updated', 'deleted'
    description = models.TextField(blank=True)
    model_type = models.CharField(max_length=100, blank=True)  # e.g. 'Book', 'Student'
    model_id = models.PositiveIntegerField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} — {self.action} {self.model_type} #{self.model_id}"
