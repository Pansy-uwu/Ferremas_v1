from django import forms
from .models import Producto, Consulta

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['nombre', 'email', 'mensaje']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'descripcion', 'precio', 'marca', 'stock', 'disponible', 'imagen', 'categoria']
