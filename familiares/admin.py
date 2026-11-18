from django.contrib import admin
from .models import Familiar

@admin.register(Familiar)
class FamiliarAdmin(admin.ModelAdmin):
    list_display = (
        'rut',
        'primer_nombre',
        'segundo_nombre',
        'apellido_paterno',
        'apellido_materno',
        'telefono',
        'correo',
    )
