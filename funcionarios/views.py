from django.shortcuts import render, redirect
from residentes.models import Residente
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CrearFuncionarioForm, IniciarSesionFuncionario, ActuaFuncionarioForm

# Create your views here.

def base(request):
    return render(request,"base.html")

@login_required
def inicio(request):
    residentes = (
        Residente.objects
        .filter(funcionario=request.user)
        .annotate(
            pendientes=Count(
                'recordatorios__fechas',
                filter=Q(recordatorios__fechas__cumplido=False),
            )
        )
        .order_by('primer_nombre')
    )
    return render(request, "inicio.html", {
        "datUsu": request.user,
        "residentes": residentes,
    })


def iniciarSesion(request):
    if request.method == "POST":
        form = IniciarSesionFuncionario(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["rut"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("funcionarios:funcionario")
            messages.error(request, "El RUT o la contraseña no son correctos.")
    else:
        form = IniciarSesionFuncionario()
    return render(request, "iniciarses.html", {"form": form})

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