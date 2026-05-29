"""
Modelo de Cliente
"""
from django.db import models


class Cliente(models.Model):
    """
    Tabla: reservas_cliente
    Personas que hacen reservas en el hotel.
    """
    nombre    = models.CharField(max_length=150)
    telefono  = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    correo    = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} — {self.correo}'
