from rest_framework import serializers
from .models import (
    AcademicYear, GradeLevel, Section, Student,
    Transaction, Fine, Payment, Reservation
)


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = ['id', 'year', 'is_current']


class GradeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeLevel
        fields = ['id', 'name']


class SectionSerializer(serializers.ModelSerializer):
    grade_level_name = serializers.CharField(source='grade_level.name', read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'name', 'grade_level', 'grade_level_name']


class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    grade_level_name = serializers.CharField(source='grade_level.name', read_only=True, default='')
    section_name = serializers.CharField(source='section.name', read_only=True, default='')

    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'first_name', 'last_name', 'full_name',
            'grade_level', 'grade_level_name',
            'section', 'section_name',
            'contact', 'guardian_name', 'guardian_contact',
            'created_at', 'updated_at',
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'fine', 'amount', 'paid_date', 'method']


class FineSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Fine
        fields = ['id', 'transaction', 'amount', 'reason', 'status', 'payments', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    book_title = serializers.CharField(source='book_copy.book.title', read_only=True)
    accession_number = serializers.CharField(source='book_copy.accession_number', read_only=True)
    fines = FineSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'book_copy', 'student',
            'student_name', 'book_title', 'accession_number',
            'issued_by', 'issued_date', 'due_date', 'returned_date',
            'status', 'notes', 'fines', 'created_at',
        ]
        read_only_fields = ['issued_by', 'issued_date']


class IssueBookSerializer(serializers.Serializer):
    """Serializer for issuing a book."""
    book_copy_id = serializers.IntegerField()
    student_id = serializers.IntegerField()
    due_date = serializers.DateField()
    notes = serializers.CharField(required=False, allow_blank=True, default='')


class ReturnBookSerializer(serializers.Serializer):
    """Serializer for returning a book."""
    transaction_id = serializers.IntegerField()
    notes = serializers.CharField(required=False, allow_blank=True, default='')


class ReservationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'book', 'student',
            'student_name', 'book_title',
            'status', 'reserved_date',
        ]
