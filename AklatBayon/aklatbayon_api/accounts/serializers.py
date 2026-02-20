from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Role, Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'slug', 'group']


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        many=True, write_only=True, source='permissions', required=False
    )

    class Meta:
        model = Role
        fields = ['id', 'name', 'slug', 'description', 'permissions', 'permission_ids', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    role_detail = RoleSerializer(source='role', read_only=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'role', 'role_detail', 'phone',
            'is_active', 'password', 'date_joined',
        ]
        read_only_fields = ['date_joined']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        
        role = validated_data.get('role')
        if role:
            role_slug = role.slug
            if role_slug in ['librarian', 'student_assistant', 'student']:
                validated_data['user_type'] = role_slug
            elif role_slug == 'administrator':
                validated_data['user_type'] = 'staff'
            elif role_slug == 'faculty':
                validated_data['user_type'] = 'teacher'

        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        role = validated_data.get('role', instance.role)
        if role:
            role_slug = role.slug
            if role_slug in ['librarian', 'student_assistant', 'student']:
                validated_data['user_type'] = role_slug
            elif role_slug == 'administrator':
                validated_data['user_type'] = 'staff'
            elif role_slug == 'faculty':
                validated_data['user_type'] = 'teacher'

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('Invalid credentials.')
        if not user.is_active:
            raise serializers.ValidationError('Account is disabled.')
        data['user'] = user
        return data
