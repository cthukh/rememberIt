from django.urls import path

from . import views

app_name = "funcionario" 

urlpatterns = [
    path('', views.inicio_residentes, name="inicio_residentes"),
    path('actualizar/',views.update_residente, name="actualizar"),
]
