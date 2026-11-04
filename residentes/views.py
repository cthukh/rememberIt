from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Residente
from .forms import ActualizarResidenteForm


def inicio_residentes(request):
    residentes = Residente.objects.all()
    residentes_asignados = Residente.objects.filter(funcionario__rut=request.user.rut)
    print(residentes_asignados)
    return render (
            request, 'inicio_residentes.html', 
            {
                'residentes': residentes, 
                'residentes_asignados': residentes_asignados,
            }
        )

def detalle_residente(request, uuid):
    residente = get_object_or_404(Residente.objects.prefetch_related('recordatorios__fechas'),uuid=uuid)
    if not residente.familiar:
        messages.warning(request, "Aún no se ha asignado un familiar para este residente")
    if not residente.funcionario:
        messages.warning(request, "Aún no se ha asignado un funcionario para este residente")
    return render(request, 'detalle_residente.html', {'residente': residente})

def update_residente(request, uuid):
    residente = get_object_or_404(Residente, uuid=uuid)
    if request.method == 'POST':
    
        form = ActualizarResidenteForm(request.POST, instance=residente)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Residente modificado con exito!")
            return redirect('residentes:detalle_residente', uuid=uuid)
        else:
            messages.error(request, "¡Ocurrio un error al modificar residente!")
            return redirect('residentes:detalle_residente', uuid=uuid)
    else:
        form = ActualizarResidenteForm(instance=residente)
    return render(request, 'modificar_residente.html', {'form': form})
