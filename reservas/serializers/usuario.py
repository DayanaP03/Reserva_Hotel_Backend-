from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from reservas.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, label='Confirmar contraseña')

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'password2', 'rol']

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({'password': 'Las contraseñas no coinciden.'})
        return attrs

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)
