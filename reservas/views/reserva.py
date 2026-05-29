from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from reservas.models import Reserva, Factura
from reservas.serializers import (
    ReservaListSerializer,
    ReservaDetailSerializer,
    ReservaCreateSerializer,
    FacturaSerializer,
)


@extend_schema(tags=['Reservas'])
class ReservaViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de Reservas.
    POST /api/reservas/{id}/cancelar/   — Cancela una reserva activa
    POST /api/reservas/{id}/finalizar/  — Marca la reserva como finalizada
    POST /api/reservas/{id}/facturar/   — Genera la factura de la reserva
    """
    queryset = Reserva.objects.select_related('cliente', 'habitacion').prefetch_related('servicios')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields   = ['cliente__nombre', 'habitacion__numero', 'estado']
    ordering_fields = ['created_at', 'fecha_entrada', 'fecha_salida']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ReservaCreateSerializer
        if self.action == 'retrieve':
            return ReservaDetailSerializer
        return ReservaListSerializer

    @extend_schema(summary='Cancelar una reserva')
    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        reserva = self.get_object()
        if reserva.estado != 'activa':
            return Response({'error': 'Solo se pueden cancelar reservas activas.'}, status=status.HTTP_400_BAD_REQUEST)
        reserva.estado = 'cancelada'
        reserva.save()
        reserva.habitacion.estado = 'disponible'
        reserva.habitacion.save()
        return Response({'mensaje': f'Reserva #{reserva.pk} cancelada exitosamente.'})

    @extend_schema(summary='Finalizar una reserva (check-out)')
    @action(detail=True, methods=['post'])
    def finalizar(self, request, pk=None):
        reserva = self.get_object()
        if reserva.estado != 'activa':
            return Response({'error': 'Solo se pueden finalizar reservas activas.'}, status=status.HTTP_400_BAD_REQUEST)
        reserva.estado = 'finalizada'
        reserva.save()
        reserva.habitacion.estado = 'disponible'
        reserva.habitacion.save()
        return Response({'mensaje': f'Reserva #{reserva.pk} finalizada. Habitación liberada.'})

    @extend_schema(summary='Generar factura para la reserva')
    @action(detail=True, methods=['post'])
    def facturar(self, request, pk=None):
        reserva = self.get_object()
        if hasattr(reserva, 'factura'):
            return Response({'error': 'Esta reserva ya tiene una factura.'}, status=status.HTTP_400_BAD_REQUEST)
        factura = Factura.objects.create(reserva=reserva, total=reserva.total)
        serializer = FacturaSerializer(factura)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
