from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ProductoViewSet
from .views import home, ContactoView, ContactoGraciasView, lista_productos, categoria, detalle_producto,agregar_al_carrito, ver_carrito, procesar_pago

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('api/', include(router.urls)),
    path('lista_de_productos', lista_productos, name='lista_productos'),
    path('categoria/<slug:slug>/', categoria, name='categoria'),
    path('producto/<int:producto_id>/', detalle_producto, name='detalle_producto'),
    path('agregar_al_carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('procesar_pago/', procesar_pago, name='procesar_pago'),
    path('contacto/', ContactoView.as_view(), name='contacto'),
    path('contacto/gracias/', ContactoGraciasView.as_view(), name='contacto_gracias'),
]
