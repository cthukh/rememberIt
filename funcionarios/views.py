from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import CrearFuncionarioForm, IniciarSesionFuncionario, ActuaFuncionarioForm,ActuaFuncionarioFormAdmin
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
    if not request.user.is_active:
        return HttpResponse("Te desactivaron la cuenta chaval")

    if request.method == "POST" and request.POST.get("accion") == "desactivar":
        if not request.user.is_superuser:
            raise PermissionDenied
        desactivados = Funcionario.objects.filter(
            pk__in=request.POST.getlist("funcionarios"), is_active=True
        ).exclude(pk=request.user.pk).update(is_active=False)
        if desactivados:
            messages.success(request, f"Se desactivaron {desactivados} funcionario(s).")
        else:
            messages.error(request, "Selecciona funcionarios activos para desactivar.")
        return redirect("funcionario:funcionario")

    datosUsuario = request.user 
    funcionarios = None
    if request.user.is_superuser:
        funcionarios = Funcionario.objects.select_related("rol").order_by(
            "last_name", "first_name"
        )

    return render(
        request,
        "inicio.html",
        {"datUsu": datosUsuario, "funcionarios": funcionarios},
    )


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
    funcionario = Funcionario.objects.obtener_por_username(username)
    if funcionario is None:
        raise Http404("Funcionario no encontrado.")
    if funcionario != request.user and not request.user.is_superuser:
        raise PermissionDenied

    if request.user.is_superuser:
        form = ActuaFuncionarioFormAdmin(instance=funcionario)
    else:
        form = ActuaFuncionarioForm(instance=funcionario)
                
    return render(request, "perfil.html", {"funcionario": funcionario, "form": form})

@login_required
def modificarFuncionario(request, username):
    funcionario = Funcionario.objects.obtener_por_username(username)
    if funcionario is None:
        raise Http404("Funcionario no encontrado.")
    if funcionario != request.user and not request.user.is_superuser:
        raise PermissionDenied
    if request.method != "POST":
        return redirect("funcionario:perfil", username=username)

    form_class = ActuaFuncionarioFormAdmin if request.user.is_superuser else ActuaFuncionarioForm
    form = form_class(request.POST, instance=funcionario)
    if form.is_valid():
        form.save()
        messages.success(request, "Tus datos de perfil se actualizaron correctamente.")
        return redirect("funcionario:perfil", username=username)

    return render(request, "perfil.html", {"funcionario": funcionario, "form": form})


