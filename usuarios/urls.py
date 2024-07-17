from django.urls import path
from .views import registro_cliente, crear_usuario_administrador, login_view, logout_view, cambiar_password_inicial, confirmar_pago, registrar_entrega

urlpatterns = [
    path('registro_cliente/', registro_cliente, name='registro_cliente'),
    path('crear_usuario_administrador/', crear_usuario_administrador, name='crear_usuario_administrador'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_change/', cambiar_password_inicial, name='password_change'),
    path('admin_home/', crear_usuario_administrador, name='admin_home'),
     path('confirmar_pago/<int:pedido_id>/', confirmar_pago, name='confirmar_pago'),
    path('registrar_entrega/<int:pedido_id>/', registrar_entrega, name='registrar_entrega'),
]
