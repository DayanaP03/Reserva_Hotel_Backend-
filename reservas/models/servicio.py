"""
Modelo de Servicio adicional del hotel
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Servicio(models.Model):
    """
    Tabla: reservas_servicio
    Servicios adicionales que el hotel ofrece (desayuno, spa, parking, etc.).
    """
    nombre      = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    precio      = models.DecimalField(
        max_digits=8, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    activo      = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} (${self.precio})'
