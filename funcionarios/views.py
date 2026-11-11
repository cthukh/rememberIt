from django.shortcuts import render, redirect, get_object_or_404
from residentes.models import Residente
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Funcionario
from administracion.forms import ActualizarFuncionarioForm
from .forms import IniciarSesionFuncionario

def base(request):
    return render(request,"base.html")

@login_required
def inicio(request):
    residentes = Residente.objects.filter(funcionario=request.user)

    if request.user.is_superuser == True:
        return render(request, "inicio_funcionario.html", {
            "datUsu": request.user,
            "residentes": residentes,
        })

    else:
        return render(request, "inicio_funcionario.html", {
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
    return render(request, "iniciar_sesion.html", {"form": form})

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
