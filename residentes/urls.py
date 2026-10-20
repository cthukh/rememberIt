from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path("nuevo/",views.registrar_residente, name="registrar_residente"),
]
