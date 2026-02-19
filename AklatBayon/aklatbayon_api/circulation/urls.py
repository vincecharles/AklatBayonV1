from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'fines', views.FineViewSet)
router.register(r'reservations', views.ReservationViewSet)
router.register(r'academic-years', views.AcademicYearViewSet)
router.register(r'grade-levels', views.GradeLevelViewSet)
router.register(r'sections', views.SectionViewSet)

urlpatterns = [
    path('circulation/issue/', views.issue_book, name='issue-book'),
    path('circulation/return/', views.return_book, name='return-book'),
    path('sections/by-grade/<int:grade_level_id>/', views.sections_by_grade, name='sections-by-grade'),
    path('', include(router.urls)),
]
