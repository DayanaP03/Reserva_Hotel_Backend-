from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from reservas.models.cliente import Cliente
from reservas.serializers.usuario import UsuarioSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['rol'] = user.rol
        token['is_staff'] = user.is_staff
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # usuario autenticado
        user = self.user

        # datos del usuario
        data['user'] = UsuarioSerializer(user).data

        # buscar cliente relacionado por correo
        cliente_id = None
        try:
            cliente = Cliente.objects.get(correo=user.email)
            cliente_id = cliente.id
        except Cliente.DoesNotExist:
            cliente_id = None

        # agregar al response
        data['cliente_id'] = cliente_id
        data['user_id'] = user.id

        return data