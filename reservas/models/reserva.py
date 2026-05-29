"""
Modelo de Reserva
"""
from django.db import models
from .cliente import Cliente
from .habitacion import Habitacion
from .servicio import Servicio


class Reserva(models.Model):
    """
    Tabla: reservas_reserva
    Registro central de cada reserva realizada en el hotel.
    """
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]

    cliente      = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='reservas')
    habitacion   = models.ForeignKey(Habitacion, on_delete=models.PROTECT, related_name='reservas')
    servicios    = models.ManyToManyField(Servicio, blank=True, related_name='reservas')
    fecha_entrada = models.DateField()
    fecha_salida  = models.DateField()
    estado        = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')
    observaciones = models.TextField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-created_at']

    def __str__(self):
        return f'Reserva #{self.pk} — {self.cliente.nombre} ({self.fecha_entrada} → {self.fecha_salida})'

    @property
    def noches(self):
        """Calcula el número de noches de la estadía."""
        return (self.fecha_salida - self.fecha_entrada).days

    @property
    def subtotal_habitacion(self):
        """Costo base de la habitación."""
        return self.habitacion.precio_noche * self.noches

    @property
    def subtotal_servicios(self):
        """Suma de todos los servicios adicionales."""
        return sum(s.precio for s in self.servicios.all())

    @property
    def total(self):
        """Total completo de la reserva."""
        return self.subtotal_habitacion + self.subtotal_servicios
