from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q, Prefetch, Exists, OuterRef
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from residentes.models import Residente
from recordatorios.models import Recordatorio, FechaRecordatorio 
from .forms import IniciarSesionFuncionario, ActuaFuncionarioForm
from .models import Funcionario

def base(request):
    return render(request,"base.html")

@login_required
@login_required
def inicio(request):
    hoy = timezone.localdate()

    fechas_hoy = FechaRecordatorio.objects.filter(fecha_hora__date=hoy)

    recordatorios_hoy = Recordatorio.objects.filter(
        Exists(FechaRecordatorio.objects.filter(recordatorio=OuterRef('pk'),fecha_hora__date=hoy,)))

    residentes = (
        Residente.objects
        .filter(funcionario=request.user)
        .annotate(
            pendientes=Count(
                'recordatorios__fechas',
                filter=Q(
                    recordatorios__fechas__fecha_hora__date=hoy,
                    recordatorios__fechas__cumplido=False,
                ),
            )
        )
        .prefetch_related(Prefetch('recordatorios', queryset=recordatorios_hoy),Prefetch('recordatorios__fechas', queryset=fechas_hoy),)
        .order_by('primer_nombre'))

    return render(request, "inicio_funcionario.html", {"datUsu": request.user,"residentes": residentes,})

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
    if user != request.user:
        return redirect("funcionarios:funcionario")
    form = ActuaFuncionarioForm(instance=user)
    return render(request, "perfil_funcionario.html", {"user": user, "form": form,"uuid":uuid})
