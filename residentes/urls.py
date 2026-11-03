from django.urls import path

from . import views

app_name = "residentes" 

urlpatterns = [
    path('', views.inicio_residentes, name="inicio_residentes"),
    path('detalle_residente/<uuid:uuid>', views.detalle_residente, name="detalle_residente" ),
    path('actualizar_residente/<uuid:uuid>', views.update_residente , name="actualizar_residente"),
]
