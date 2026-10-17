from django.urls import path
from . import views

app_name = "funcionario"

urlpatterns = [
    path('',views.inicio,name="funcionario"),
    path('registro/',views.registro, name="registro")

]
