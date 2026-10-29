from django.urls import path

from . import views

app_name = "residentes" 

urlpatterns = [
    path('residente/', views.inicio_residentes, name="inicio_residentes"),
    path('crear_residente', views.crear_residente, name="crear_residente"),
    path('detalle_residente/<uuid:uuid>', views.detalle_residente, name="detalle_residente" ),
    path('actualizar_residente/<uuid:uuid>', views.update_residente , name="actualizar_residente"),
]
