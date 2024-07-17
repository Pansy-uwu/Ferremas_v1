# productos/admin.py
from django.contrib import admin
from .models import Categoria, Producto, Consulta

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Consulta)
