# 🏨 Hoteles API — Backend Django REST

Sistema de Reservas de Hoteles construido con **Django 4.2 + Django REST Framework + JWT**.

---

## 📁 Estructura de mi Proyecto Reserva de Hotel

```
hoteles_api/
├── .github/workflows/deploy.yml   # Deploy automático al VPS
├── .venv/                          # Entorno virtual de Python
├── config/
│   ├── settings.py                 # Configuración general
│   ├── urls.py                     # Rutas principales
│   └── wsgi.py                     # Servidor de producción (Gunicorn)
├── reservas/                       # App principal
│   ├── migrations/                 # Historial de cambios en la BD
│   ├── models/
│   │   ├── usuario.py              # Usuarios del sistema (Admin / Recepcionista)
│   │   ├── cliente.py              # Clientes del hotel
│   │   ├── habitacion.py           # Habitaciones (simple, doble, suite)
│   │   ├── servicio.py             # Servicios adicionales (desayuno, spa...)
│   │   ├── reserva.py              # Reservas (FK a cliente + habitación)
│   │   └── factura.py              # Facturas y Pagos
│   ├── serializers/                # Conversión Modelos ↔ JSON
│   ├── views/                      # Controladores de los endpoints
│   ├── urls.py                     # Rutas de la API
│   └── admin.py                    # Panel de administración
├── .env.example                    # Variables de entorno (copiar a .env)
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🗄️ Tablas de la Base de Datos

| Tabla               | Descripción                                  |
|---------------------|----------------------------------------------|
| `reservas_usuario`  | Administradores y Recepcionistas del sistema |
| `reservas_cliente`  | Clientes que hacen reservas                  |
| `reservas_habitacion` | Habitaciones del hotel (simple/doble/suite)|
| `reservas_servicio` | Servicios adicionales (desayuno, spa, etc.)  |
| `reservas_reserva`  | Reservas (une cliente + habitación)          |
| `reservas_factura`  | Facturas generadas por reservas              |
| `reservas_pago`     | Pagos registrados contra facturas            |

---

## 🚀 Instalación y Configuración

### 1. Clonar e instalar dependencias
```bash
git clone <tu-repositorio>
cd hoteles_api
python -m venv .venv
source .venv/bin/activate       

pip install -r requirements.txt
```

### 2. Configurar variables de entorno
```bash
cp .env.example .env

```

### 3. Crear la base de datos en PostgreSQL
```sql
CREATE DATABASE hoteles_db;
```

### 4. Aplicar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario (administrador)
```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor
```bash
python manage.py runserver
```

---

## 🔗 Endpoints de la API

Base URL: `http://localhost:8000/api/`

### 🔐 Autenticación
| Método | Ruta                  | Descripción                          | Auth |
|--------|-----------------------|--------------------------------------|------|
| POST   | `/auth/login/`        | Obtener token JWT (access + refresh) | No   |
| POST   | `/auth/refresh/`      | Renovar access token                 | No   |
| POST   | `/auth/registro/`     | Crear nuevo usuario del sistema      | No   |
| GET    | `/auth/perfil/`       | Ver datos del usuario actual         | Sí   |

### 👥 Clientes
| Método | Ruta                  | Descripción           |
|--------|-----------------------|-----------------------|
| GET    | `/clientes/`          | Listar clientes       |
| POST   | `/clientes/`          | Crear cliente         |
| GET    | `/clientes/{id}/`     | Detalle de cliente    |
| PUT    | `/clientes/{id}/`     | Actualizar cliente    |
| DELETE | `/clientes/{id}/`     | Eliminar cliente      |

### 🛏️ Habitaciones
| Método | Ruta                           | Descripción                    |
|--------|--------------------------------|--------------------------------|
| GET    | `/habitaciones/`               | Listar habitaciones            |
| POST   | `/habitaciones/`               | Crear habitación               |
| GET    | `/habitaciones/{id}/`          | Detalle de habitación          |
| PUT    | `/habitaciones/{id}/`          | Actualizar habitación          |
| GET    | `/habitaciones/disponibles/`   | Solo habitaciones disponibles  |

### 🎯 Reservas
| Método | Ruta                           | Descripción                       |
|--------|--------------------------------|-----------------------------------|
| GET    | `/reservas/`                   | Listar reservas                   |
| POST   | `/reservas/`                   | Crear reserva                     |
| GET    | `/reservas/{id}/`              | Detalle de reserva                |
| POST   | `/reservas/{id}/cancelar/`     | Cancelar reserva                  |
| POST   | `/reservas/{id}/finalizar/`    | Check-out (finalizar)             |
| POST   | `/reservas/{id}/facturar/`     | Generar factura                   |

### 🧾 Facturas y Pagos
| Método | Ruta                                 | Descripción              |
|--------|--------------------------------------|--------------------------|
| GET    | `/facturas/`                         | Listar facturas          |
| GET    | `/facturas/{id}/`                    | Detalle de factura       |
| POST   | `/facturas/{id}/registrar-pago/`     | Registrar un pago        |
| GET    | `/pagos/`                            | Historial de pagos       |

---

## 📚 Documentación Interactiva

Una vez el servidor esté corriendo:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Panel Admin**: http://localhost:8000/admin/

---

## 🔑 Uso del Token JWT

```bash
# 1. Obtener token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hotel.com", "password": "tu_contraseña"}'

# 2. Usar el token en peticiones protegidas
curl http://localhost:8000/api/reservas/ \
  -H "Authorization: Bearer <access_token>"
```

---

## 🏭 Producción con Gunicorn

```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```
