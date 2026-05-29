from rest_framework import serializers
from reservas.models import Factura, Pago


class PagoSerializer(serializers.ModelSerializer):
    metodo_display = serializers.CharField(source='get_metodo_pago_display', read_only=True)

    class Meta:
        model = Pago
        fields = ['id', 'factura', 'metodo_pago', 'metodo_display', 'monto', 'fecha_pago', 'referencia']
        read_only_fields = ['id', 'fecha_pago']


class FacturaSerializer(serializers.ModelSerializer):
    pagos           = PagoSerializer(many=True, read_only=True)
    estado_display  = serializers.CharField(source='get_estado_pago_display', read_only=True)
    total_pagado    = serializers.SerializerMethodField()
    saldo_pendiente = serializers.SerializerMethodField()

    class Meta:
        model = Factura
        fields = [
            'id', 'reserva', 'total', 'fecha_emision',
            'estado_pago', 'estado_display', 'notas',
            'pagos', 'total_pagado', 'saldo_pendiente',
        ]
        read_only_fields = ['id', 'fecha_emision']

    def get_total_pagado(self, obj):
        return sum(p.monto for p in obj.pagos.all())

    def get_saldo_pendiente(self, obj):
        return obj.total - self.get_total_pagado(obj)
