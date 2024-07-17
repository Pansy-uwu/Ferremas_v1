from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'descripcion', 'precio', 'marca', 'stock', 'disponible', 'imagen', 'categoria']
