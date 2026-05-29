"""
Modelo de Usuario Personalizado
Reemplaza al User de Django para añadir el campo 'rol'.
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio.')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'administrador')
        return self.create_user(email, username, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Tabla: reservas_usuario
    Usuarios del sistema (Administradores y Recepcionistas).
    """
    ROL_CHOICES = [
        ('administrador', 'Administrador'),
        ('recepcionista', 'Recepcionista'),
    ]

    username   = models.CharField(max_length=50, unique=True)
    email      = models.EmailField(unique=True)
    rol        = models.CharField(max_length=20, choices=ROL_CHOICES, default='recepcionista')
    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.username} ({self.get_rol_display()})'
