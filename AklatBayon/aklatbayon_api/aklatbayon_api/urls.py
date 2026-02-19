"""
Main URL configuration for aklatbayon_api.
All API routes are prefixed with /api/
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT token refresh
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # App routes
    path('api/', include('accounts.urls')),
    path('api/', include('library.urls')),
    path('api/', include('circulation.urls')),
    path('api/', include('system.urls')),
]
