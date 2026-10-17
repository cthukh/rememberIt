from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login

from .forms import CrearUsuarioForm
# Create your views here.


def inicio(request):
    if not request.user.is_authenticated:
        return redirect("funcionario:registro")
    return render(request,"inicio.html")



def registro(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            usuario =  form.save()
            usuario.save()
            login(request,usuario)
            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect("funcionario/")  # Ajusta según tu URL de login
        else:
            messages.error(request, "Por favor corrige los errores.")
    else:
        form = CrearUsuarioForm()
    return render(request,"registro.html",{"form":form})