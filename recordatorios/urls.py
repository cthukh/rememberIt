from django.urls import path

from . import views

app_name = "recordatorios" 

urlpatterns = [
    path('crear_recordatorio/<uuid:uuid>', views.crear_recordatorio, name="crear_recordatorio"),
    path('detalle_recordatorio/<uuid:uuid>', views.detalle_recordatorio, name="detalle_recordatorio"),
]
