from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from residentes.models import Residente
from .forms import CrearRecordatorioForm
from .models import FechaRecordatorio, Recordatorio
from .utils import generar_fechas
from django.contrib.auth.decorators import login_required

@login_required
def crear_recordatorio(request, uuid):
    residente = get_object_or_404(Residente, uuid=uuid)
    if request.method == 'POST':
        form = CrearRecordatorioForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                recordatorio = form.save(commit=False)
                recordatorio.residente = residente
                recordatorio.save()
                FechaRecordatorio.objects.bulk_create([
                    FechaRecordatorio(recordatorio=recordatorio, fecha_hora=f)
                    for f in generar_fechas(recordatorio)
                ])
            return redirect('residentes:detalle_residente', uuid=residente.uuid)
    else:
        form = CrearRecordatorioForm()

    return render(request, 'crear_recordatorio.html', {'form': form,'residente': residente,})

@login_required
def detalle_recordatorio(request, uuid):
    recordatorio = get_object_or_404(Recordatorio, uuid=uuid)
    return render(request, 'detalle_recordatorio.html', {'recordatorio':recordatorio})