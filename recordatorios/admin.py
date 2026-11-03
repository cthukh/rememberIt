from django.contrib import admin
from .models import Recordatorio, FechaRecordatorio

# Register your models here.
@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'nombre',
        'descripcion',
        'frecuencia',
        'fecha_inicio',
        'fecha_fin',
        'residente',
    )

@admin.register(FechaRecordatorio)
class FechaRecordatorioAdmin(admin.ModelAdmin):
    list_display = (
        'recordatorio',
        'fecha_hora',
        'cumplido',
    )