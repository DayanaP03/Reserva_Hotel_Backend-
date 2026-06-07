"""
Rutas de la API — Sistema de Reservas de Hoteles
"""
from turtle import home

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from reservas.views import (
    LoginView, RegistroView, PerfilView,
    ClienteViewSet, HabitacionViewSet, ServicioViewSet,
    ReservaViewSet, FacturaViewSet, PagoViewSet,
)
from reservas.views.admin import AdminUserList, AdminUserUpdate

router = DefaultRouter()
router.register(r'clientes',    ClienteViewSet,    basename='cliente')
router.register(r'habitaciones', HabitacionViewSet, basename='habitacion')
router.register(r'servicios',   ServicioViewSet,   basename='servicio')
router.register(r'reservas',    ReservaViewSet,    basename='reserva')
router.register(r'facturas',    FacturaViewSet,    basename='factura')
router.register(r'pagos',       PagoViewSet,       basename='pago')

urlpatterns = [
    # Autenticación
     path('', home),  
    path('auth/login/',    LoginView.as_view(),   name='login'),
    path('auth/refresh/',  TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/registro/', RegistroView.as_view(), name='registro'),
    path('auth/perfil/',   PerfilView.as_view(),   name='perfil'),
    # Admin user management
    path('admin/users/', AdminUserList.as_view(), name='admin-user-list'),
    path('admin/users/<int:pk>/', AdminUserUpdate.as_view(), name='admin-user-update'),

    # Recursos principales
    path('', include(router.urls)),
]
