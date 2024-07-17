from django.contrib import admin
from .models import Pedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'producto', 'cantidad', 'metodo_entrega', 'opcion_pago', 'direccion_entrega', 'estado', 'estado_pago')
    list_filter = ('estado', 'estado_pago', 'metodo_entrega', 'opcion_pago')
    search_fields = ('usuario__username', 'producto__nombre', 'direccion_entrega')
