from django.urls import path

from . import views

app_name = "residentes" 

urlpatterns = [
    path('', views.inicio_residentes, name="inicio_residentes"),
    path('residente/crear_residente', views.crear_residente, name="crear_residente"),
    path('residente/detalle_residente/<uuid:uuid>', views.detalle_residente, name="detalle_residente" ),
    path('residente/actualizar_residente/<uuid:uuid>', views.update_residente , name="actualizar_residente"),
]
