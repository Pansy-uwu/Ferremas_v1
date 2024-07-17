from django.shortcuts import render, redirect
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions, IntegrationCommerceCodes, IntegrationApiKeys
from transbank.common.integration_type import IntegrationType
from pedidos.models import Pedido
from productos.models import Producto

# Configura los detalles de integración con Webpay
commerce_code = IntegrationCommerceCodes.WEBPAY_PLUS
api_key = IntegrationApiKeys.WEBPAY
options = WebpayOptions(commerce_code=commerce_code, api_key=api_key, integration_type=IntegrationType.TEST)

def respuesta_pago(request):
    token_ws = request.POST.get('token_ws')
    if not token_ws:
        token_ws = request.GET.get('token_ws')

    if not token_ws:
        return render(request, 'webpay/failure.html', {'response': 'Token no encontrado'})

    tx = Transaction(options=options)
    response = tx.commit(token_ws)
    
    if response['status'] == 'AUTHORIZED':
        # Recupera los datos del pedido de la sesión
        buy_order = request.session.get('buy_order')
        amount = request.session.get('amount')
        metodo_entrega = request.session.get('metodo_entrega')
        opcion_pago = request.session.get('opcion_pago')
        direccion_entrega = request.session.get('direccion_entrega')
        carrito = request.session.get('carrito', {})

        # Crea los pedidos
        for producto_id, cantidad in carrito.items():
            producto = Producto.objects.get(id=producto_id)
            pedido = Pedido(
                usuario=request.user,
                producto=producto,
                cantidad=cantidad,
                metodo_entrega=metodo_entrega,
                opcion_pago=opcion_pago,
                direccion_entrega=direccion_entrega if metodo_entrega == 'despacho' else '',
                estado_pago='pagado'  # Marcar el pedido como pagado
            )
            pedido.save()

        # Limpiar el carrito
        request.session['carrito'] = {}
        return render(request, 'webpay/success.html', {'response': response})
    else:
        return render(request, 'webpay/failure.html', {'response': response})
