from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CrearFuncionarioForm, IniciarSesionFuncionario

# Create your views here.

def base(request):
    return render(request,"base.html")

def inicio(request):
    if not request.user.is_authenticated:
        return redirect("funcionario:iniciar_sesion")
    return render(request,"inicio.html")


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