from rest_framework import viewsets, filters
from drf_spectacular.utils import extend_schema
from reservas.models import Servicio
from reservas.serializers import ServicioSerializer


@extend_schema(tags=['Servicios'])
class ServicioViewSet(viewsets.ModelViewSet):
    """CRUD completo de Servicios adicionales del hotel."""
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields   = ['nombre']
