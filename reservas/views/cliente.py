from rest_framework import viewsets, filters
from drf_spectacular.utils import extend_schema
from reservas.models import Cliente
from reservas.serializers import ClienteSerializer


@extend_schema(tags=['Clientes'])
class ClienteViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de Clientes.
    GET    /api/clientes/       — Lista todos los clientes
    POST   /api/clientes/       — Crea un cliente
    GET    /api/clientes/{id}/  — Detalle de un cliente
    PUT    /api/clientes/{id}/  — Actualiza un cliente
    DELETE /api/clientes/{id}/  — Elimina un cliente
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields   = ['nombre', 'correo', 'telefono']
    ordering_fields = ['nombre', 'created_at']
