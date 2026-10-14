from django.contrib import admin
from .models import Residente

# Register your models here.
@admin.register(Residente)
class ResidenteAdmin(admin.ModelAdmin):
    list_display = ('rut','primer_nombre','segundo_nombre','apellido_paterno','apellido_materno','edad','alergias','telefono_emergencias','funcionario','familiar','fecha_creacion')
    