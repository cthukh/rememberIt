from django.shortcuts import render, redirect, get_object_or_404
from residentes.models import Residente
from django.db.models import Count, Q
from django.http import Http404, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from administracion.forms import ActualizarFuncionarioForm
from .forms import IniciarSesionFuncionario
from .models import Funcionario
from core.validators import normalizar_rut

# Create your views here.

def base(request):
    return render(request,"base.html")
@login_required
def bitacora(request):
    return render(request,"bitacora.html")
@login_required
def pizarra(request):
    return render(request,"pizarra.html")

@login_required
def visitas(request):
    return render(request, "agendaVisitas.html")

@login_required
def recepcion(request):
    return render(request, "recepcion.html")

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
                return redirect("funcionarios:funcionario")
            messages.error(request, "El RUT o la contraseña no son correctos.")
    else:
        form = IniciarSesionFuncionario()
    return render(request, "iniciar_sesion.html", {"form": form})

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
    return redirect("funcionarios:iniciar_sesion")

@login_required
def perfil(request,uuid):
    user = get_object_or_404(Funcionario, uuid=uuid)
    form = ActualizarFuncionarioForm(instance=user)
    # Si no es superusuario, todo en solo lectura
    if request.user is not None and not request.user.is_superuser:
        for field in form.fields.values():
            field.disabled = True

    return render(
        request, 
        "perfil_funcionario.html", 
        {
            "user": user, 
            "form": form,
            "uuid": uuid,
        }
    )
