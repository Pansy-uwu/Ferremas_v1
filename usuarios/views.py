from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm, AdminUserCreationForm
from .models import CustomUser
from pedidos.models import Pedido

def registro_cliente(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'cliente'
            user.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/registro_cliente.html', {'form': form})

@login_required
def crear_usuario_administrador(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            rut = form.cleaned_data['rut']
            user.set_password(f"{user.username}{rut}")  # Configura una contraseña inicial basada en el username y RUT
            user.save()
            return redirect('admin_home')
    else:
        form = AdminUserCreationForm()
    return render(request, 'usuarios/crear_usuario_administrador.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Verifica si el administrador tiene la contraseña inicial
            if user.role == 'administrador' and user.check_password(f"{user.username}{user.rut}"):
                return redirect('password_change')
            return redirect('admin_home' if user.role == 'administrador' else 'home')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def cambiar_password_inicial(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantener al usuario logueado después de cambiar la contraseña
            return redirect('admin_home')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'usuarios/cambiar_password_inicial.html', {'form': form})

@login_required
def admin_home(request):
    return render(request, 'usuarios/admin_home.html')

def confirmar_pago(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.pago_confirmado = True
    pedido.save()
    return redirect('lista_pedidos')

def registrar_entrega(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.entregado = True
    pedido.save()
    return redirect('lista_pedidos')
