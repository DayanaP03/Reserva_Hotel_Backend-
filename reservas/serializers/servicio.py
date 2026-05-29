from rest_framework import serializers
from reservas.models import Servicio


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'descripcion', 'precio', 'activo']
        read_only_fields = ['id']
