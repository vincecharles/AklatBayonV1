from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Role, Permission
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer, LoginSerializer



@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Authenticate user and return JWT tokens."""
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data,
    })


@api_view(['POST'])
def logout_view(request):
    """Blacklist the refresh token."""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'detail': 'Logged out successfully.'})
    except Exception:
        return Response({'detail': 'Logged out.'})


@api_view(['GET'])
def me_view(request):
    """Return current authenticated user profile."""
    return Response(UserSerializer(request.user).data)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('role').all()
    serializer_class = UserSerializer
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'date_joined', 'user_type']



class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.prefetch_related('permissions').all()
    serializer_class = RoleSerializer

    @action(detail=True, methods=['get', 'put'], url_path='permissions')
    def manage_permissions(self, request, pk=None):
        role = self.get_object()
        if request.method == 'GET':
            all_permissions = Permission.objects.all()
            role_perm_ids = set(role.permissions.values_list('id', flat=True))
            data = []
            for perm in all_permissions:
                data.append({
                    **PermissionSerializer(perm).data,
                    'enabled': perm.id in role_perm_ids,
                })
            return Response(data)

        perm_ids = request.data.get('permission_ids', [])
        role.permissions.set(perm_ids)
        return Response({'detail': 'Permissions updated.', 'permissions': PermissionSerializer(role.permissions.all(), many=True).data})


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
