from django.urls import path

from . import views

app_name = "recordatorios" 

urlpatterns = [
    path('crear_recordatorio/<str:uuid>', views.crear_recordatorio, name="crear_recordatorio"),
]
