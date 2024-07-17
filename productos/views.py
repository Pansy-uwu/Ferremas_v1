from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Producto, SubCategoria
from pedidos.models import Pedido
from .forms import ConsultaForm
import requests
from requests.exceptions import RequestException
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions, IntegrationCommerceCodes, IntegrationApiKeys
from transbank.common.integration_type import IntegrationType
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages

class ContactoView(FormView):
    template_name = 'productos/contacto.html'
    form_class = ConsultaForm
    success_url = reverse_lazy('contacto_gracias')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class ContactoGraciasView(TemplateView):
    template_name = 'productos/contacto_gracias.html'

def obtener_dolar():
    try:
        response = requests.get('https://mindicador.cl/api')
        indicadores = response.json()
        dolar = Decimal(indicadores['dolar']['valor'])
        return dolar
    except RequestException:
        return 850.0 # Valor predeterminado en caso de fallo en la conexión

def home(request):
    dolar = obtener_dolar()
    promociones = Producto.objects.filter(disponible=True).order_by('-id')[:5]
    lanzamientos = Producto.objects.filter(disponible=True).order_by('-id')[:5]
    productos = Producto.objects.filter(disponible=True)
    return render(request, 'productos/home.html', {
        'promociones': promociones, 
        'lanzamientos': lanzamientos,
        'productos': productos,
        'dolar': dolar
    })

def lista_productos(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    dolar = obtener_dolar()
    return render(request, 'productos/lista_productos.html', {'categorias': categorias, 'productos': productos, 'dolar': dolar})

def categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    productos = Producto.objects.filter(categoria=categoria)
    subcategorias = SubCategoria.objects.filter(categoria=categoria)
    dolar = obtener_dolar()
    return render(request, 'productos/categoria.html', {'categoria': categoria, 'productos': productos, 'subcategorias': subcategorias, 'dolar': dolar})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    dolar = obtener_dolar()
    return render(request, 'productos/detalle_producto.html',{'producto': producto, 'dolar': dolar})

def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    carrito[producto_id] = carrito.get(producto_id, 0) + 1
    request.session['carrito'] = carrito
    return redirect(reverse('home') + '#todos-productos')

@login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    
    if request.method == 'POST':
        producto_id = int(request.POST.get('producto_id'))
        action = request.POST.get('action')
        if action == 'increase':
            carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1
        elif action == 'decrease':
            if carrito.get(str(producto_id), 0) > 1:
                carrito[str(producto_id)] -= 1
            else:
                carrito.pop(str(producto_id), None)
        elif action == 'delete':
            carrito.pop(str(producto_id), None)
        request.session['carrito'] = carrito
        return redirect('ver_carrito')

    productos = Producto.objects.filter(id__in=carrito.keys())
    total_clp = sum(Decimal(producto.precio) * Decimal(cantidad) for producto, cantidad in zip(productos, carrito.values()))
    dolar = obtener_dolar()
    total_usd = total_clp / Decimal(dolar)
    
    carrito_items = []
    for producto in productos:
        carrito_items.append({
            'producto': producto,
            'cantidad': carrito[str(producto.id)]
        })
    
    return render(request, 'productos/ver_carrito.html', {
        'carrito_items': carrito_items, 
        'total_clp': total_clp, 
        'total_usd': total_usd, 
        'dolar': dolar
    })



# Configura los detalles de integración con Webpay
commerce_code = IntegrationCommerceCodes.WEBPAY_PLUS
api_key = IntegrationApiKeys.WEBPAY
options = WebpayOptions(commerce_code=commerce_code, api_key=api_key, integration_type=IntegrationType.TEST)

@login_required
def procesar_pago(request):
    if request.method == 'POST':
        metodo_entrega = request.POST.get('metodo_entrega')
        opcion_pago = request.POST.get('opcion_pago')
        direccion_entrega = request.POST.get('direccion_entrega', '')

        if metodo_entrega == 'despacho' and not direccion_entrega.strip():
            messages.error(request, 'La dirección de entrega es obligatoria para el despacho a domicilio.')
            return redirect('ver_carrito')

        carrito = request.session.get('carrito', {})
        total_clp = sum(Decimal(Producto.objects.get(id=producto_id).precio) * Decimal(cantidad) for producto_id, cantidad in carrito.items())
        total_clp = float(total_clp)  # Convertir a float para evitar problemas de serialización

        if opcion_pago == 'transferencia':
            # Manejar el caso de transferencia
            for producto_id, cantidad in carrito.items():
                producto = Producto.objects.get(id=producto_id)
                Pedido.objects.create(
                    usuario=request.user,
                    producto=producto,
                    cantidad=cantidad,
                    metodo_entrega=metodo_entrega,
                    opcion_pago=opcion_pago,
                    direccion_entrega=direccion_entrega,
                    estado='pendiente',
                    estado_pago='pendiente'
                )
            request.session['carrito'] = {}
            return render(request, 'productos/mensaje_transferencia.html', {'total_clp': total_clp})

        buy_order = str(request.user.id) + str(total_clp)
        session_id = request.session.session_key
        return_url = request.build_absolute_uri('/webpay/response/')

        tx = Transaction(options=options)
        response = tx.create(buy_order, session_id, total_clp, return_url)

        # Guarda los detalles del pedido en la sesión
        request.session['buy_order'] = buy_order
        request.session['amount'] = total_clp
        request.session['metodo_entrega'] = metodo_entrega
        request.session['opcion_pago'] = opcion_pago
        request.session['direccion_entrega'] = direccion_entrega

        return render(request, 'webpay/pago.html', {'response': response})

    return redirect('ver_carrito')
