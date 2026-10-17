from django import forms
from .models import Funcionario
from django.contrib.auth.forms import UserCreationForm
class CrearUsuarioForm(UserCreationForm):

    class Meta:
        model= Funcionario
        fields =('rut','first_name','last_name','email')
