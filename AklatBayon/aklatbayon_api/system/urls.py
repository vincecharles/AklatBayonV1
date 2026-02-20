from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'settings', views.SettingViewSet)
router.register(r'audit-logs', views.ActivityLogViewSet)

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    path('remote-migrate/', views.remote_migrate, name='remote_migrate'),
    path('create-remote-superuser/', views.create_remote_superuser, name='create_remote_superuser'),
    path('remote-seed/', views.remote_seed, name='remote_seed'),
    path('', include(router.urls)),
]
