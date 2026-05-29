"""
Modelo de Habitación
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Habitacion(models.Model):
    """
    Tabla: reservas_habitacion
    Las habitaciones disponibles en el hotel.
    """
    TIPO_CHOICES = [
        ('simple', 'Simple'),
        ('doble', 'Doble'),
        ('suite', 'Suite'),
    ]
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('mantenimiento', 'En Mantenimiento'),
    ]

    numero       = models.CharField(max_length=10, unique=True)
    tipo         = models.CharField(max_length=20, choices=TIPO_CHOICES)
    precio_noche = models.DecimalField(
        max_digits=8, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    estado       = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    descripcion  = models.TextField(blank=True)
    capacidad    = models.PositiveSmallIntegerField(default=2)

    class Meta:
        verbose_name = 'Habitación'
        verbose_name_plural = 'Habitaciones'
        ordering = ['numero']

    def __str__(self):
        return f'Habitación {self.numero} — {self.get_tipo_display()} (${self.precio_noche}/noche)'
