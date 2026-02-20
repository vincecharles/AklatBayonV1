from django.db.models import Count, Q, Sum
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Setting, ActivityLog
from .serializers import SettingSerializer, ActivityLogSerializer
from library.models import Book, BookCopy
from circulation.models import Transaction, Fine, Student



@api_view(['GET'])
def dashboard(request):
    """Dashboard statistics."""
    data = {
        'total_books': Book.objects.count(),
        'total_copies': BookCopy.objects.count(),
        'available_copies': BookCopy.objects.filter(status='available').count(),
        'issued_copies': BookCopy.objects.filter(status='issued').count(),
        'total_students': Student.objects.count(),
        'active_loans': Transaction.objects.filter(status='issued').count(),
        'overdue_loans': Transaction.objects.filter(status='overdue').count(),
        'pending_fines': Fine.objects.filter(status='pending').count(),
        'total_fines_amount': Fine.objects.filter(status='pending').aggregate(
            total=Sum('amount')
        )['total'] or 0,
    }
    return Response(data)



@api_view(['GET'])
def reports(request):
    """Report dashboard with summary data."""
    report_type = request.query_params.get('type', 'summary')

    if report_type == 'circulation':
        data = Transaction.objects.values('status').annotate(count=Count('id'))
    elif report_type == 'fines':
        data = Fine.objects.values('status').annotate(
            count=Count('id'),
            total_amount=Sum('amount'),
        )
    elif report_type == 'books_by_category':
        data = Book.objects.values('category__name').annotate(count=Count('id')).order_by('-count')
    elif report_type == 'most_borrowed':
        data = Transaction.objects.values(
            'book_copy__book__title'
        ).annotate(
            borrow_count=Count('id')
        ).order_by('-borrow_count')[:10]
    else:
        data = {
            'total_books': Book.objects.count(),
            'total_students': Student.objects.count(),
            'total_transactions': Transaction.objects.count(),
            'total_fines_collected': Fine.objects.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0,
        }

    return Response(data)



class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer



class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.select_related('user').all()
    serializer_class = ActivityLogSerializer
    search_fields = ['action', 'description', 'model_type', 'user__username']
    ordering_fields = ['created_at']



@api_view(['GET'])
@permission_classes([AllowAny])
def remote_migrate(request):
    """Run database migrations remotely."""
    try:
        call_command('migrate', interactive=False)
        return JsonResponse({'status': 'success', 'message': 'Migrations executed successfully.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_remote_superuser(request):
    """Create a superuser remotely. For initial setup only."""
    User = get_user_model()
    
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not password or not email:
        return JsonResponse({'status': 'error', 'message': 'username, email, and password required'}, status=400)
        
    try:
        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'User already exists'}, status=400)
            
        User.objects.create_superuser(username=username, email=email, password=password)
        return JsonResponse({'status': 'success', 'message': f'Superuser {username} created successfully.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

