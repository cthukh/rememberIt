from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio_residentes, name="inicio_residentes"),
    path('actualizar/',views.update_residente, name="actualizar"),
]
