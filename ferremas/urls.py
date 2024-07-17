from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="FERREMAS API",
      default_version='v1',
      description="Documentación de la API de FERREMAS",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@ferremas.cl"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('productos/', include('productos.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('webpay/', include('webpay.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include('productos.urls')),  # Ruta raíz apuntando a la vista home
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
