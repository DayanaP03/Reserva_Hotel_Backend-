from pathlib import Path
from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.http import FileResponse, Http404
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


def download_apk(request):
    apk_file = Path(settings.BASE_DIR) / 'apk' / 'hotel.apk'
    if not apk_file.exists():
        raise Http404('Archivo APK no encontrado. Por favor coloca hotel.apk en la carpeta apk/.')
    return FileResponse(
        open(apk_file, 'rb'),
        as_attachment=True,
        filename='hotel.apk',
        content_type='application/vnd.android.package-archive'
    )

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('reservas.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]