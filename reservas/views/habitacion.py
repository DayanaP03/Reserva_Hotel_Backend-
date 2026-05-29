from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from reservas.models import Habitacion
from reservas.serializers import HabitacionSerializer


@extend_schema(tags=['Habitaciones'])
class HabitacionViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de Habitaciones.
    GET /api/habitaciones/disponibles/ — Solo habitaciones disponibles
    """
    queryset = Habitacion.objects.all()
    serializer_class = HabitacionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields   = ['numero', 'tipo', 'estado']
    ordering_fields = ['numero', 'precio_noche', 'tipo']

    @extend_schema(summary='Listar solo habitaciones disponibles')
    @action(detail=False, methods=['get'], url_path='disponibles')
    def disponibles(self, request):
        """GET /api/habitaciones/disponibles/"""
        qs = Habitacion.objects.filter(estado='disponible')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
