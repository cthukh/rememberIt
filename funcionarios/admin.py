from django.contrib import admin
from .models import Rol, Funcionario

# Register your models here.

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('rol_id', 'nombre')
    
@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('rut','primer_nombre','segundo_nombre','apellido_paterno','apellido_materno','direccion','telefono','correo','rol','fecha_creacion','objects')