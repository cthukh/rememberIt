from django.urls import path
from . import views

app_name = "funcionario"

urlpatterns = [
    path('',views.inicio,name="funcionario"),
    path('registro/',views.registro, name="registro"),
    path('base/',views.base),
    path('iniciarSesion/', views.iniciarSesion, name='iniciar_sesion'),
    path('cerrarSesion/', views.cerrarSesion, name='cerrar_sesion'),
    path('perfil/',views.perfil,name="perfil"),
    path('agregarNumero/',views.modificarFuncionario,name="agregarNumero")

]
