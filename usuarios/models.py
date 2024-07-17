from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role_choices = [
        ('cliente', 'Cliente'),
        ('administrador', 'Administrador'),
        ('vendedor', 'Vendedor'),
        ('bodeguero', 'Bodeguero'),
        ('contador', 'Contador'),
    ]
    role = models.CharField(max_length=15, choices=role_choices)
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)  # Temporalmente anulable


    def __str__(self):
        return self.username or ""
