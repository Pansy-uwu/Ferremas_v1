from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Introduzca una dirección de correo electrónico válida.")
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class AdminUserCreationForm(UserCreationForm):
    rut = forms.CharField(max_length=12, required=True, help_text="Requerido. Introduzca el RUT sin puntos y con guion.")
    role = forms.ChoiceField(choices=CustomUser.role_choices, required=True, help_text="Seleccione el rol del usuario.")
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'rut', 'role', 'password1', 'password2')
