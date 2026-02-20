from django.db import models
from django.conf import settings


class AcademicYear(models.Model):
    year = models.CharField(max_length=20, unique=True)  # e.g. "2025-2026"
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return self.year

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicYear.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class GradeLevel(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g. "Grade 7"

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=100)
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, related_name='sections')

    class Meta:
        ordering = ['grade_level', 'name']
        unique_together = ['name', 'grade_level']

    def __str__(self):
        return f"{self.grade_level.name} - {self.name}"


class Student(models.Model):
    student_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.SET_NULL, null=True, related_name='students')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    contact = models.CharField(max_length=100, blank=True)
    guardian_name = models.CharField(max_length=255, blank=True)
    guardian_contact = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.student_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Transaction(models.Model):
    """Book issue/return tracking."""
    class Status(models.TextChoices):
        ISSUED = 'issued', 'Issued'
        RETURNED = 'returned', 'Returned'
        OVERDUE = 'overdue', 'Overdue'
        LOST = 'lost', 'Lost'

    book_copy = models.ForeignKey('library.BookCopy', on_delete=models.CASCADE, related_name='transactions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='transactions')
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='issued_transactions')
    issued_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ISSUED)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-issued_date']

    def __str__(self):
        return f"{self.student} ← {self.book_copy} ({self.status})"


class Fine(models.Model):
    """Fine for overdue/lost/damaged books."""
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'
        WAIVED = 'waived', 'Waived'

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='fines')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fine ₱{self.amount} - {self.status}"


class Payment(models.Model):
    fine = models.ForeignKey(Fine, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, default='cash')

    def __str__(self):
        return f"Payment ₱{self.amount} for Fine #{self.fine.pk}"


class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        FULFILLED = 'fulfilled', 'Fulfilled'
        CANCELLED = 'cancelled', 'Cancelled'

    book = models.ForeignKey('library.Book', on_delete=models.CASCADE, related_name='reservations')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='reservations')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    reserved_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-reserved_date']

    def __str__(self):
        return f"{self.student} → {self.book} ({self.status})"
