from django.shortcuts import render, get_object_or_404, redirect
from .models import Residente
from .forms import CrearResidenteForm,ActuaResidenteForm


def inicio_residentes(request):
    
    residentes = Residente.objects.all()
    
    
    return render(request, 'inicio_residentes.html',{'residentes': residentes})


def crear_residente(request):
    
    if request.method == 'POST':
        form = CrearResidenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio_residentes')
    else:
        form = CrearResidenteForm()
    
    return render(request, 'crear_cuenta.html', {'form': form})

def detalle_residente(request, uuid):
    
    
    return render(request, 'detalle_residente.html')

def update_residente(request, uuid):
    
    residente = get_object_or_404(Residente, uuid=uuid)
    
    if request.method == 'POST':
    
        form = ActuaResidenteForm(request.POST, instance=residente)
        if form.is_valid():
            form.save()
            return redirect('residentes:inicio_residentes')
    else:
        form = ActuaResidenteForm(instance=residente)
    
    
    return render(request, 'updateresidente.html', {'form': form})