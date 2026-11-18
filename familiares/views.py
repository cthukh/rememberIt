from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from .forms import IniciarSesionFamiliar, RegistrarFamiliarForm
from .models import Familiar
from .decorators import familiar_requerido


def index(request):
    return render(request, 'index.html')

def iniciar_sesion_familiar(request):
    if request.method == "POST":
        form = IniciarSesionFamiliar(request.POST)
        if form.is_valid():
            rut = form.cleaned_data["rut"]
            password = form.cleaned_data["password"]

            try:
                familiar = Familiar.objects.get(rut=rut)
            except Familiar.DoesNotExist:
                familiar = None

            if familiar and check_password(password, familiar.password):
                request.session.flush()  # limpia cualquier sesión anterior
                request.session["familiar_rut"] = familiar.rut
                return redirect("familiares:home")

            # mismo mensaje para RUT inexistente o clave mala
            messages.error(request, "El RUT o la contraseña no son correctos.")
    else:
        form = IniciarSesionFamiliar()
    return render(request, "iniciar_sesion_familiar.html", {"form": form})

def registrar_familiar(request):
    if request.method == 'POST':
        form = RegistrarFamiliarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada con éxito.")
            return redirect("familiares:home")
        else:
            messages.error(request, "¡Ocurrió un error al crear la cuenta!")
            # sin redirect: se muestra el form con sus errores
    else:
        form = RegistrarFamiliarForm()
    return render(request, "registrar_familiar.html", {"form": form})

@familiar_requerido
def inicio_familiar(request): # home
    return render(request, 'inicio_familiar.html')

def cerrar_sesion(request):
    request.session.flush()
    return redirect("familiares:index")