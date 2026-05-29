from rest_framework import serializers
from reservas.models import Habitacion


class HabitacionSerializer(serializers.ModelSerializer):
    tipo_display   = serializers.CharField(source='get_tipo_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = Habitacion
        fields = [
            'id', 'numero', 'tipo', 'tipo_display',
            'precio_noche', 'estado', 'estado_display',
            'descripcion', 'capacidad',
        ]
        read_only_fields = ['id']
