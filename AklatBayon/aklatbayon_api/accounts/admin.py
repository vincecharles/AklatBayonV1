from django.contrib import admin
from .models import User, Role, Permission


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type', 'role', 'is_active']
    list_filter = ['user_type', 'role', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    filter_horizontal = ['permissions']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'group']
    list_filter = ['group']
