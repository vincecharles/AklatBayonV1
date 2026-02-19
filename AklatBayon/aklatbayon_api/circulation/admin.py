from django.contrib import admin
from .models import (
    AcademicYear, GradeLevel, Section, Student,
    Transaction, Fine, Payment, Reservation,
)


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['year', 'is_current']


@admin.register(GradeLevel)
class GradeLevelAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade_level']
    list_filter = ['grade_level']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'last_name', 'first_name', 'grade_level', 'section']
    list_filter = ['grade_level']
    search_fields = ['student_id', 'first_name', 'last_name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['student', 'book_copy', 'status', 'issued_date', 'due_date']
    list_filter = ['status']


@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'amount', 'status']
    list_filter = ['status']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['fine', 'amount', 'paid_date', 'method']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['book', 'student', 'status', 'reserved_date']
    list_filter = ['status']
