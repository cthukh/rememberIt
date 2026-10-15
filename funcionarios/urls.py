from django.urls import path
from . import views
urlpatterns = [
    path('',views.registroFuncionario,name="registro_funcionario")
]
