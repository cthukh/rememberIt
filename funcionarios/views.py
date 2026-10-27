from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import CrearFuncionarioForm, IniciarSesionFuncionario, ActuaFuncionarioForm
from .models import Funcionario
from core.validators import normalizar_rut

# Create your views here.

def base(request):
    return render(request,"base.html")

@login_required
def inicio(request):
    print(request.user.username)
    if not request.user.is_authenticated:
        return redirect("funcionario:iniciar_sesion")
    datosUsuario = request.user 

    return render(request,"inicio.html",{"datUsu":datosUsuario})


def iniciarSesion(request):
    if request.method == "POST":
        form = IniciarSesionFuncionario(request.POST)
        if form.is_valid():
            identificador = form.cleaned_data["identificador"].strip()
            if "@" in identificador:
                funcionario = Funcionario.objects.filter(
                    email__iexact=identificador,
                ).first()
            else:
                funcionario = Funcionario.objects.filter(
                    rut=normalizar_rut(identificador),
                ).first()

            user = None
            if funcionario is not None:
                user = authenticate(
                    request,
                    username=funcionario.rut,
                    password=form.cleaned_data["password"],
                )
            if user is not None:
                login(request, user)
                return redirect("funcionario:funcionario")
            messages.error(request, "El correo/RUT o la contraseña no son correctos.")
    else:
        form = IniciarSesionFuncionario()
    return render(request, "iniciarses.html", {"form": form})


def recuperarContrasena(request):
    vista = auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy("funcionario:password_reset_done"),
    )
    return vista(request)


def recuperacionEnviada(request):
    return auth_views.PasswordResetDoneView.as_view()(request)


def confirmarContrasena(request, uidb64, token):
    vista = auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy("funcionario:password_reset_complete"),
    )
    return vista(request, uidb64=uidb64, token=token)


def contrasenaRestablecida(request):
    return auth_views.PasswordResetCompleteView.as_view()(request)


@login_required
def cerrarSesion(request):
    logout(request)
    return redirect("funcionario:iniciar_sesion")


def registro(request):
    if request.method == 'POST':
        form = CrearFuncionarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "Tu cuenta está lista. Bienvenido/a.")
            return redirect("funcionario:funcionario")
        else:
            messages.error(request, "Por favor corrige los errores.")
    else:
        form = CrearFuncionarioForm()
    return render(request,"registro.html",{"form":form})

@login_required
def perfil(request,username):
    username = request.user.username
    datosUsuario = request.user
    form = ActuaFuncionarioForm(instance=datosUsuario)
    return render(request, "perfil.html", {"datUsu": datosUsuario, "form": form,"username":username})

@login_required
def modificarFuncionario(request):
    if request.method != "POST":
        return redirect("funcionario:perfil")

    form = ActuaFuncionarioForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Tus datos de perfil se actualizaron correctamente.")
        return redirect("funcionario:perfil")

    return render(request, "perfil.html", {"datUsu": request.user, "form": form})