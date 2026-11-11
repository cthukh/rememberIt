from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from residentes.models import Residente
from .forms import CrearRecordatorioForm
from .models import FechaRecordatorio, Recordatorio
from .utils import generar_fechas


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
@require_POST
def marcar_cumplido(request, fecha_id):
    fecha = get_object_or_404(
        FechaRecordatorio,
        id=fecha_id,
        recordatorio__residente__funcionario=request.user,
    )

    if not fecha.cumplido:
        fecha.cumplido = True
        fecha.save(update_fields=["cumplido"])
        messages.success(
            request,
            f"{fecha.recordatorio.nombre} de las {fecha.fecha_hora:%H:%M} marcado como realizado."
        )

    return redirect("funcionarios:funcionario")

@login_required
def modi_recordatorio(request, uuid):
    recordatorio = get_object_or_404(
        Recordatorio,
        uuid=uuid,
        residente__funcionario=request.user,   # solo SUS residentes
    )

    if request.method == 'POST':
        form = CrearRecordatorioForm(request.POST, instance=recordatorio)
        if form.is_valid():
            with transaction.atomic():
                recordatorio = form.save()

                # Solo regenero fechas si cambió algo del horario
                campos_horario = {'frecuencia', 'indefinido', 'fecha_inicio', 'fecha_fin'}
                if campos_horario & set(form.changed_data):
                    ahora = timezone.now()

                    # 1. borro solo las pendientes futuras (el historial se queda)
                    recordatorio.fechas.filter(cumplido=False, fecha_hora__gte=ahora).delete()

                    # 2. genero las nuevas, saltando las que ya existen
                    existentes = set(recordatorio.fechas.values_list('fecha_hora', flat=True))
                    nuevas = [
                        FechaRecordatorio(recordatorio=recordatorio, fecha_hora=f)
                        for f in generar_fechas(recordatorio)
                        if f >= ahora and f not in existentes
                    ]
                    FechaRecordatorio.objects.bulk_create(nuevas)

            messages.success(request, "Recordatorio actualizado.")
            return redirect("funcionarios:funcionario")
    else:
        form = CrearRecordatorioForm(instance=recordatorio)

    return render(request, 'crear_recordatorio.html', {
        'form': form,
        'residente': recordatorio.residente,
        'editando': True,
    })


@login_required
@require_POST
def eliminar_recordatorio(request, uuid):
    recordatorio = get_object_or_404(
        Recordatorio,
        uuid=uuid,
        residente__funcionario=request.user,
    )
    nombre = recordatorio.nombre
    recordatorio.delete()
    messages.success(request, f"Recordatorio «{nombre}» eliminado.")
    return redirect("funcionarios:funcionario")

@login_required
def eventos_calendario(request, uuid):
    residente = get_object_or_404(Residente, uuid=uuid, funcionario=request.user)

    fechas = FechaRecordatorio.objects.filter(
        recordatorio__residente=residente
    ).select_related("recordatorio")

    # FullCalendar manda start y end del mes que se está viendo
    inicio = parse_datetime(request.GET.get("start", ""))
    fin = parse_datetime(request.GET.get("end", ""))
    if inicio and fin:
        fechas = fechas.filter(fecha_hora__gte=inicio, fecha_hora__lt=fin)

    eventos = [
        {
            "id": f.id,
            "title": f.recordatorio.nombre,
            "start": timezone.localtime(f.fecha_hora).isoformat(),
            "color": "#2f7d5b" if f.cumplido else "#d9a520",
        }
        for f in fechas
    ]
    return JsonResponse(eventos, safe=False)