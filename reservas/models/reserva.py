from django.db import models
from .cliente import Cliente
from .habitacion import Habitacion
from .servicio import Servicio


class Reserva(models.Model):

    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='reservas'
    )

    habitacion = models.ForeignKey(
        Habitacion,
        on_delete=models.PROTECT,
        related_name='reservas'
    )

    servicios = models.ManyToManyField(
        Servicio,
        blank=True,
        related_name='reservas'
    )

    fecha_entrada = models.DateField(null=True, blank=True)
    fecha_salida = models.DateField(null=True, blank=True)

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='activa'
    )

    observaciones = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-created_at']

    def __str__(self):
        return f'Reserva #{self.pk} — {self.cliente}'

    @property
    def noches(self):
        if not self.fecha_entrada or not self.fecha_salida:
            return 0
        return (self.fecha_salida - self.fecha_entrada).days

    @property
    def subtotal_habitacion(self):
        if not self.habitacion or not self.fecha_entrada or not self.fecha_salida:
            return 0
        return self.habitacion.precio_noche * self.noches

    @property
    def subtotal_servicios(self):
        if not self.pk:
            return 0
        return sum(s.precio for s in self.servicios.all())

    @property
    def total(self):
        return self.subtotal_habitacion + self.subtotal_servicios