from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from .models import (
    AcademicYear, GradeLevel, Section, Student,
    Transaction, Fine, Payment, Reservation,
)
from .serializers import (
    AcademicYearSerializer, GradeLevelSerializer, SectionSerializer,
    StudentSerializer, TransactionSerializer,
    FineSerializer, PaymentSerializer, ReservationSerializer,
    IssueBookSerializer, ReturnBookSerializer,
)
from library.models import BookCopy


# ──────────── Academic ────────────

class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer


class GradeLevelViewSet(viewsets.ModelViewSet):
    queryset = GradeLevel.objects.all()
    serializer_class = GradeLevelSerializer


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.select_related('grade_level').all()
    serializer_class = SectionSerializer


@api_view(['GET'])
def sections_by_grade(request, grade_level_id):
    """Get sections for a specific grade level."""
    sections = Section.objects.filter(grade_level_id=grade_level_id)
    return Response(SectionSerializer(sections, many=True).data)


# ──────────── Students ────────────

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('grade_level', 'section').all()
    serializer_class = StudentSerializer
    search_fields = ['student_id', 'first_name', 'last_name']
    ordering_fields = ['last_name', 'student_id', 'created_at']


# ──────────── Circulation ────────────

@api_view(['POST'])
def issue_book(request):
    """Issue a book copy to a student."""
    serializer = IssueBookSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        book_copy = BookCopy.objects.get(id=serializer.validated_data['book_copy_id'])
    except BookCopy.DoesNotExist:
        return Response({'error': 'Book copy not found.'}, status=status.HTTP_404_NOT_FOUND)

    if book_copy.status != 'available':
        return Response({'error': 'Book copy is not available.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        student = Student.objects.get(id=serializer.validated_data['student_id'])
    except Student.DoesNotExist:
        return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)

    transaction = Transaction.objects.create(
        book_copy=book_copy,
        student=student,
        issued_by=request.user,
        due_date=serializer.validated_data['due_date'],
        notes=serializer.validated_data.get('notes', ''),
        status='issued',
    )

    # Mark book copy as issued
    book_copy.status = 'issued'
    book_copy.save()

    return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def return_book(request):
    """Return a book."""
    serializer = ReturnBookSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        transaction = Transaction.objects.get(id=serializer.validated_data['transaction_id'])
    except Transaction.DoesNotExist:
        return Response({'error': 'Transaction not found.'}, status=status.HTTP_404_NOT_FOUND)

    if transaction.status == 'returned':
        return Response({'error': 'Book already returned.'}, status=status.HTTP_400_BAD_REQUEST)

    # Update transaction
    transaction.status = 'returned'
    transaction.returned_date = timezone.now()
    transaction.notes = serializer.validated_data.get('notes', transaction.notes)
    transaction.save()

    # Mark book copy as available
    book_copy = transaction.book_copy
    book_copy.status = 'available'
    book_copy.save()

    # Auto-create fine if overdue
    if transaction.due_date < timezone.now().date():
        from django.conf import settings as app_settings
        days_overdue = (timezone.now().date() - transaction.due_date).days
        fine_per_day = 5.00  # ₱5 per day — can be moved to Settings model
        Fine.objects.create(
            transaction=transaction,
            amount=days_overdue * fine_per_day,
            reason=f'Overdue by {days_overdue} day(s)',
        )

    return Response(TransactionSerializer(transaction).data)


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """View transaction history."""
    queryset = Transaction.objects.select_related('book_copy__book', 'student', 'issued_by').prefetch_related('fines').all()
    serializer_class = TransactionSerializer
    search_fields = ['student__first_name', 'student__last_name', 'book_copy__book__title']
    ordering_fields = ['issued_date', 'due_date', 'status']


# ──────────── Fines ────────────

class FineViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Fine.objects.select_related('transaction__student', 'transaction__book_copy__book').prefetch_related('payments').all()
    serializer_class = FineSerializer

    @action(detail=True, methods=['post'])
    def collect(self, request, pk=None):
        """Collect payment for a fine."""
        fine = self.get_object()
        if fine.status != 'pending':
            return Response({'error': 'Fine is not pending.'}, status=status.HTTP_400_BAD_REQUEST)

        amount = request.data.get('amount', fine.amount)
        method = request.data.get('method', 'cash')

        Payment.objects.create(fine=fine, amount=amount, method=method)
        fine.status = 'paid'
        fine.save()

        return Response(FineSerializer(fine).data)

    @action(detail=True, methods=['post'])
    def waive(self, request, pk=None):
        """Waive a fine."""
        fine = self.get_object()
        if fine.status != 'pending':
            return Response({'error': 'Fine is not pending.'}, status=status.HTTP_400_BAD_REQUEST)

        fine.status = 'waived'
        fine.save()

        return Response(FineSerializer(fine).data)


# ──────────── Reservations ────────────

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related('book', 'student').all()
    serializer_class = ReservationSerializer
