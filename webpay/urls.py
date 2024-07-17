from django.urls import path
from .views import respuesta_pago

urlpatterns = [
    path('response/', respuesta_pago, name='respuesta_pago'),
]
