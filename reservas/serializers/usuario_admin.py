from rest_framework import serializers
from reservas.models import Usuario


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol', 'is_active', 'is_staff']
        read_only_fields = ['id', 'username', 'email']
