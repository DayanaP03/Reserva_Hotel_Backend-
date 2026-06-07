from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from reservas.serializers import UsuarioSerializer, RegistroUsuarioSerializer
from reservas.serializers.auth import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


@extend_schema(tags=['Autenticación'])
class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Devuelve access token y refresh token.
    """
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(tags=['Autenticación'])
class RegistroView(generics.CreateAPIView):
    """
    POST /api/auth/registro/
    Crea un nuevo usuario del sistema.
    """
    serializer_class = RegistroUsuarioSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['Autenticación'])
class PerfilView(APIView):
    """
    GET /api/auth/perfil/
    Devuelve los datos del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)
