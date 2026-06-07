from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from reservas.models import Usuario
from reservas.serializers.usuario_admin import UserAdminSerializer


class AdminUserList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = Usuario.objects.all().order_by('-created_at')
        serializer = UserAdminSerializer(users, many=True)
        return Response(serializer.data)


class AdminUserUpdate(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            user = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserAdminSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
