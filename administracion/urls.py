from django.urls import path
from . import views

app_name = "administracion" 

urlpatterns = [
    path('', views.inicio_admin, name='inicio_admin'),
    path('registrar_funcionario/',views.crear_funcionario, name="crear_funcionario"),
    path('modificar_funcionario/<uuid:uuid>', views.modificar_funcionario, name='modificar_funcionario'),
    path('registrar_residente/', views.crear_residente, name="crear_residente"),
]