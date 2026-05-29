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
    list_display  = ('id', 'cliente', 'habitacion', 'fecha_entrada', 'fecha_salida', 'estado', 'noches')
    list_filter   = ('estado', 'fecha_entrada')
    search_fields = ('cliente__nombre', 'habitacion__numero')
    readonly_fields = ('noches', 'subtotal_habitacion', 'subtotal_servicios', 'total')
    inlines       = [ReservaServiciosInline]

    def noches(self, obj):
        return obj.noches
    noches.short_description = 'Noches'


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'reserva', 'total', 'estado_pago', 'fecha_emision')
    list_filter  = ('estado_pago',)


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'factura', 'monto', 'metodo_pago', 'fecha_pago')
    list_filter  = ('metodo_pago',)
