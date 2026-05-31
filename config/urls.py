from django.http import JsonResponse
from django.urls import path, include
from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

def home(request):
    return JsonResponse({
        "status": "ok",
        "message": "API Hoteles funcionando 🚀"
    })

urlpatterns = [
    path('', home),  # 👈 esto arregla el /
    path('admin/', admin.site.urls),
    path('api/', include('reservas.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]