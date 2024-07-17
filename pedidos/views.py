from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from usuarios.decorators import vendedor_required, bodeguero_required, contador_required 
from .models import Pedido
from productos.models import Producto

@login_required
@vendedor_required
def productos_disponibles(request):
    productos = Producto.objects.filter(stock__gt=0)
    return render(request, 'pedidos/productos_disponibles.html', {'productos': productos})

@login_required
@vendedor_required
def lista_pedidos(request):
    if request.user.role != 'vendedor':
        return redirect('home')

    pedidos_pendientes = Pedido.objects.filter(estado='pendiente')
    pedidos_revisados = Pedido.objects.filter(estado__in=['aprobado', 'rechazado', 'enviado'])

    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        accion = request.POST.get('accion')
        pedido = get_object_or_404(Pedido, id=pedido_id)

        if accion == 'aprobar':
            pedido.estado = 'aprobado'
            producto = pedido.producto
            producto.stock -= pedido.cantidad
            producto.save()
        elif accion == 'rechazar':
            pedido.estado = 'rechazado'
        elif accion == 'enviar':
            pedido.estado = 'enviado'
        
        pedido.save()

    return render(request, 'pedidos/lista_pedidos.html', {
        'pedidos_pendientes': pedidos_pendientes,
        'pedidos_revisados': pedidos_revisados,
    })

@login_required
@vendedor_required
def aprobar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    if request.user.role == 'vendedor':
        pedido.estado = 'aprobado'
        producto = pedido.producto
        producto.stock -= pedido.cantidad
        producto.save()
        pedido.save()
    return redirect('lista_pedidos')

@login_required
@vendedor_required
def rechazar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    if request.user.role == 'vendedor':
        pedido.estado = 'rechazado'
        pedido.save()
    return redirect('lista_pedidos')

@login_required
@vendedor_required
def enviar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    if request.user.role == 'vendedor':
        pedido.estado = 'enviado'
        pedido.save()
    return redirect('lista_pedidos')

#Bodeguero

@login_required
@bodeguero_required
def vista_bodeguero(request):
    pedidos = Pedido.objects.filter(estado__in=['pendiente', 'aprobado', 'preparado'])
    pedidos_entregados = Pedido.objects.filter(estado='enviado')

    return render(request, 'pedidos/vista_bodeguero.html', {
        'pedidos': pedidos,
        'pedidos_entregados': pedidos_entregados,
    })

@login_required
@bodeguero_required
def aceptar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.estado = 'preparado'
    pedido.save()
    return redirect('vista_bodeguero')

@login_required
@bodeguero_required
def entregar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.estado = 'enviado'
    pedido.save()
    return redirect('vista_bodeguero')

#Contador
@login_required
@contador_required
def vista_contador(request):
    pedidos_transferencia = Pedido.objects.filter(opcion_pago='transferencia', estado_pago='pendiente')
    pedidos_entrega = Pedido.objects.filter(estado='enviado')
    pedidos_completados = Pedido.objects.filter(estado='entregado')

    return render(request, 'pedidos/vista_contador.html', {
        'pedidos_transferencia': pedidos_transferencia,
        'pedidos_entrega': pedidos_entrega,
        'pedidos_completados': pedidos_completados,
    })

@login_required
@contador_required
def confirmar_pago(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.estado_pago = 'pagado'
    pedido.save()
    return redirect('vista_contador')

@login_required
@contador_required
def registrar_entrega(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.estado = 'entregado'
    pedido.save()
    return redirect('vista_contador')