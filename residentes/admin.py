from django.contrib import admin
from .models import Residente

# Register your models here.
@admin.register(Residente)
class ResidenteAdmin(admin.ModelAdmin)