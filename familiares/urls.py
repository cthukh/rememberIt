from django.urls import path
from . import views

app_name = "familiares" 

urlpatterns = [
    path('', views.index, name='index'),
    path('inciarSesion/', views.iniciar_sesion_familiar, name='iniciar_sesion'),
    path('registrarse/', views.registrar_familiar, name='registrarse'),
    path('inicio/', views.inicio_familiar, name="home"),
    path('cerrarSesion/', views.cerrar_sesion, name="cerrar_sesion"),
]
