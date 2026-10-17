from django import forms
from .models import Funcionario
from django.contrib.auth.forms import UserCreationForm
class CrearFuncionarioForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model= Funcionario
        fields =('rut','first_name','last_name','email')


class IniciarSesionFuncionario():
    pass