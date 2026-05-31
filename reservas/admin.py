from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from reservas.models import Usuario, Cliente, Habitacion, Servicio, Reserva, Factura, Pago


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display  = ('username', 'email', 'rol', 'is_active', 'created_at')
    list_filter   = ('rol', 'is_active')
    search_fields = ('username', 'email')
    ordering      = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Rol y Permisos', {'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username', 'email', 'password1', 'password2', 'rol')}),
    )


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'correo', 'telefono', 'created_at')
    search_fields = ('nombre', 'correo')


@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display  = ('numero', 'tipo', 'precio_noche', 'estado', 'capacidad')
    list_filter   = ('tipo', 'estado')
    search_fields = ('numero',)


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'activo')
    list_filter  = ('activo',)


class ReservaServiciosInline(admin.TabularInline):
    model = Reserva.servicios.through
    extra = 0


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display  = ('id', 'cliente', 'habitacion', 'fecha_entrada', 'fecha_salida', 'estado', 'get_noches')
    list_filter   = ('estado', 'fecha_entrada')
    search_fields = ('cliente__nombre', 'habitacion__numero')
    readonly_fields = ('get_noches', 'get_subtotal_habitacion', 'get_subtotal_servicios', 'get_total')
    inlines       = [ReservaServiciosInline]

    fields = (
        'cliente', 'habitacion', 'fecha_entrada', 'fecha_salida',
        'estado', 'observaciones',
        'get_noches', 'get_subtotal_habitacion',
        'get_subtotal_servicios', 'get_total'
    )

    def get_noches(self, obj):
        if not obj or not obj.fecha_entrada or not obj.fecha_salida:
            return '—'
        return f"{obj.noches} noche(s)"
    get_noches.short_description = 'Noches'

    def get_subtotal_habitacion(self, obj):
        if not obj or not obj.fecha_entrada or not obj.fecha_salida or not obj.habitacion:
            return '—'
        return f"${obj.subtotal_habitacion:.2f}"
    get_subtotal_habitacion.short_description = 'Subtotal habitación'

    def get_subtotal_servicios(self, obj):
        if not obj or not obj.pk:
            return '—'
        return f"${obj.subtotal_servicios:.2f}"
    get_subtotal_servicios.short_description = 'Subtotal servicios'

    def get_total(self, obj):
        if not obj or not obj.fecha_entrada or not obj.fecha_salida:
            return '—'
        return f"${obj.total:.2f}"
    get_total.short_description = 'Total'


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'reserva', 'total', 'estado_pago', 'fecha_emision')
    list_filter  = ('estado_pago',)


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'factura', 'monto', 'metodo_pago', 'fecha_pago')
    list_filter  = ('metodo_pago',)