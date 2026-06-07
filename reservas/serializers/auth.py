from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from reservas.serializers.usuario import UsuarioSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Añadir claims personalizadas
        token['rol'] = user.rol
        token['is_staff'] = user.is_staff
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Añadir datos del usuario a la respuesta
        data['user'] = UsuarioSerializer(self.user).data
        return data
