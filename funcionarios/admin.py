from django.contrib import admin
from .models import Rol, Funcionario

# Register your models here.

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('rol_id', 'nombre')
    
@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('rut', 'first_name', 'last_name', 'email', 'phone_number', 'rol', 'date_joined')