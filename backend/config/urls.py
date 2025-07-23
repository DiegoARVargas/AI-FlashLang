import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView     # 🔁 Recibe refresh → devuelve nuevo access

urlpatterns = [
    path('admin-panel-1189/', admin.site.urls),
    path('api/', include('api_vocabulary.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh
    path('api-auth/', include('rest_framework.urls')),  # 👈 Esto activa el botón de login en DRF
    path('api/users/', include('users.urls')),  # Rutas de usuarios
]

# ✅ Servir archivos estáticos y multimedia tanto en desarrollo como en Render (producción)
if settings.DEBUG or os.getenv("RENDER") == "true":
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
