from django.urls import path
from .views import productos_disponibles, lista_pedidos, aprobar_pedido, rechazar_pedido, enviar_pedido, vista_bodeguero, aceptar_pedido, entregar_pedido, vista_contador, confirmar_pago, registrar_entrega

urlpatterns = [
    path('productos_disponibles/', productos_disponibles, name='productos_disponibles'),
    path('lista_pedidos/', lista_pedidos, name='lista_pedidos'),
    path('aprobar_pedido/<int:id>/', aprobar_pedido, name='aprobar_pedido'),
    path('rechazar_pedido/<int:id>/', rechazar_pedido, name='rechazar_pedido'),
    path('enviar_pedido/<int:id>/', enviar_pedido, name='enviar_pedido'),
    path('vista_bodeguero/', vista_bodeguero, name='vista_bodeguero'),
    path('aceptar_pedido/<int:id>/', aceptar_pedido, name='aceptar_pedido'),
    path('entregar_pedido/<int:id>/', entregar_pedido, name='entregar_pedido'),
    path('vista_contador/', vista_contador, name='vista_contador'),
    path('confirmar_pago/<int:id>/', confirmar_pago, name='confirmar_pago'),
    path('registrar_entrega/<int:id>/', registrar_entrega, name='registrar_entrega'),
]
