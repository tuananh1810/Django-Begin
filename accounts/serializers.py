from rest_framework import serializers
from .models import Role, Permission, User

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'code']

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True, write_only=True, source='permissions'
    )

    class Meta:
        model = Role
        fields = ['id', 'name', 'permissions', 'permission_ids']

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), write_only=True, source='role')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'role_id']
