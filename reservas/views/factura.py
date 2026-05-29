from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from reservas.models import Factura, Pago
from reservas.serializers import FacturaSerializer, PagoSerializer


@extend_schema(tags=['Facturas'])
class FacturaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Consulta y gestión de Facturas.
    Solo lectura: las facturas se crean desde el endpoint de reservas (/facturar/).
    POST /api/facturas/{id}/registrar-pago/ — Registra un pago en la factura
    """
    queryset = Factura.objects.select_related('reserva').prefetch_related('pagos')
    serializer_class = FacturaSerializer

    @extend_schema(summary='Registrar un pago en la factura', request=PagoSerializer)
    @action(detail=True, methods=['post'], url_path='registrar-pago')
    def registrar_pago(self, request, pk=None):
        factura = self.get_object()
        serializer = PagoSerializer(data={**request.data, 'factura': factura.pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Si el total pagado cubre la factura, marcamos como pagado
        total_pagado = sum(p.monto for p in factura.pagos.all())
        if total_pagado >= factura.total:
            factura.estado_pago = 'pagado'
            factura.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Pagos'])
class PagoViewSet(viewsets.ReadOnlyModelViewSet):
    """Historial de todos los pagos registrados."""
    queryset = Pago.objects.select_related('factura')
    serializer_class = PagoSerializer
