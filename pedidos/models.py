from django.db import models
from productos.models import Producto
from usuarios.models import CustomUser

class Pedido(models.Model):
    METODO_ENTREGA_CHOICES = [
        ('retiro', 'Retiro en Tienda'),
        ('despacho', 'Despacho a Domicilio'),
    ]

    OPCIONES_PAGO_CHOICES = [
        ('debito', 'Débito'),
        ('credito', 'Crédito'),
        ('transferencia', 'Transferencia'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
        ('enviado', 'Enviado'),
        ('preparado', 'Preparado'),
        ('entregado', 'Entregado'),
    ]
    
    ESTADO_PAGO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('fallido', 'Fallido'),
    ]

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    metodo_entrega = models.CharField(max_length=10, choices=METODO_ENTREGA_CHOICES, default='retiro')
    opcion_pago = models.CharField(max_length=20, choices=OPCIONES_PAGO_CHOICES, default='debito')
    direccion_entrega = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    estado_pago = models.CharField(max_length=10, choices=ESTADO_PAGO_CHOICES, default='pendiente')

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades - {self.estado} - {self.estado_pago}"

