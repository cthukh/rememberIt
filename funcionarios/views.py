from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CrearFuncionarioForm, IniciarSesionFuncionario, PerfilFuncionarioForm

# Create your views here.

def base(request):
    return render(request,"base.html")

def inicio(request):
    if not request.user.is_authenticated:
        return redirect("funcionario:iniciar_sesion")
    datosUsuario = request.user 

    return render(request,"inicio.html",{"datUsu":datosUsuario})


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
                return redirect("funcionario:funcionario")
            messages.error(request, "El RUT o la contraseña no son correctos.")
    else:
        form = IniciarSesionFuncionario()
    return render(request, "iniciarses.html", {"form": form})


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
def perfil(request):
    datosUsuario = request.user
    form = PerfilFuncionarioForm(instance=datosUsuario)
    return render(request, "perfil.html", {"datUsu": datosUsuario, "form": form})

@login_required
def agregarNumero(request):
    if request.method != "POST":
        return redirect("funcionario:perfil")

    form = PerfilFuncionarioForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Tus datos de perfil se actualizaron correctamente.")
        return redirect("funcionario:perfil")

    return render(request, "perfil.html", {"datUsu": request.user, "form": form})