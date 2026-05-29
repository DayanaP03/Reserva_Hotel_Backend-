from rest_framework import serializers
from reservas.models import Reserva
from .cliente import ClienteSerializer
from .habitacion import HabitacionSerializer
from .servicio import ServicioSerializer


class ReservaListSerializer(serializers.ModelSerializer):
    """Serializer compacto para listas."""
    cliente_nombre   = serializers.CharField(source='cliente.nombre', read_only=True)
    habitacion_numero = serializers.CharField(source='habitacion.numero', read_only=True)
    estado_display   = serializers.CharField(source='get_estado_display', read_only=True)
    noches           = serializers.IntegerField(read_only=True)
    total            = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Reserva
        fields = [
            'id', 'cliente_nombre', 'habitacion_numero',
            'fecha_entrada', 'fecha_salida', 'noches',
            'estado', 'estado_display', 'total', 'created_at',
        ]


class ReservaDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado con objetos anidados."""
    cliente    = ClienteSerializer(read_only=True)
    habitacion = HabitacionSerializer(read_only=True)
    servicios  = ServicioSerializer(many=True, read_only=True)
    noches     = serializers.IntegerField(read_only=True)
    subtotal_habitacion = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    subtotal_servicios  = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total               = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Reserva
        fields = '__all__'


class ReservaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear/actualizar reservas."""
    servicios = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=__import__('reservas.models', fromlist=['Servicio']).Servicio.objects.filter(activo=True),
        required=False
    )

    class Meta:
        model = Reserva
        fields = ['cliente', 'habitacion', 'servicios', 'fecha_entrada', 'fecha_salida', 'observaciones']

    def validate(self, attrs):
        entrada = attrs.get('fecha_entrada')
        salida  = attrs.get('fecha_salida')
        if entrada and salida and salida <= entrada:
            raise serializers.ValidationError(
                {'fecha_salida': 'La fecha de salida debe ser posterior a la de entrada.'}
            )
        habitacion = attrs.get('habitacion')
        if habitacion and habitacion.estado != 'disponible':
            raise serializers.ValidationError(
                {'habitacion': f'La habitación {habitacion.numero} no está disponible.'}
            )
        return attrs

    def create(self, validated_data):
        servicios = validated_data.pop('servicios', [])
        reserva = Reserva.objects.create(**validated_data)
        reserva.servicios.set(servicios)
        # Marcar habitación como ocupada
        reserva.habitacion.estado = 'ocupada'
        reserva.habitacion.save()
        return reserva
