"""
Modelos de Factura y Pago
"""
from django.db import models
from .reserva import Reserva


class Factura(models.Model):
    """
    Tabla: reservas_factura
    Documento de cobro generado a partir de una reserva.
    """
    ESTADO_PAGO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('anulado', 'Anulado'),
    ]

    reserva       = models.OneToOneField(Reserva, on_delete=models.PROTECT, related_name='factura')
    total         = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    estado_pago   = models.CharField(max_length=20, choices=ESTADO_PAGO_CHOICES, default='pendiente')
    notas         = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha_emision']

    def __str__(self):
        return f'Factura #{self.pk} — Reserva #{self.reserva.pk} — ${self.total}'


class Pago(models.Model):
    """
    Tabla: reservas_pago
    Registro de cada pago realizado contra una factura.
    """
    METODO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta de Crédito/Débito'),
        ('transferencia', 'Transferencia Bancaria'),
    ]

    factura     = models.ForeignKey(Factura, on_delete=models.PROTECT, related_name='pagos')
    metodo_pago = models.CharField(max_length=20, choices=METODO_CHOICES)
    monto       = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago  = models.DateTimeField(auto_now_add=True)
    referencia  = models.CharField(max_length=100, blank=True, help_text='Número de transacción o referencia del banco.')

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha_pago']

    def __str__(self):
        return f'Pago ${self.monto} ({self.get_metodo_pago_display()}) — Factura #{self.factura.pk}'
