"""
Main URL configuration for aklatbayon_api.
All API routes are prefixed with /api/
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/admin/', admin.site.urls),

    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('api/', include('accounts.urls')),
    path('api/', include('library.urls')),
    path('api/', include('circulation.urls')),
    path('api/', include('system.urls')),
]
