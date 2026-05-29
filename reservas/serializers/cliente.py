from rest_framework import serializers
from reservas.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    total_reservas = serializers.SerializerMethodField()

    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'telefono', 'direccion', 'correo', 'created_at', 'total_reservas']
        read_only_fields = ['id', 'created_at']

    def get_total_reservas(self, obj):
        return obj.reservas.count()
