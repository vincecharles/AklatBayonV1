from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'settings', views.SettingViewSet)
router.register(r'audit-logs', views.ActivityLogViewSet)

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    path('', include(router.urls)),
]
