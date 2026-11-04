from django import forms
from .models import Funcionario
from django.contrib.auth.forms import UserCreationForm

class IniciarSesionFuncionario(forms.Form):
    rut = forms.CharField(
        label="RUT",
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"autocamplete": "current-password"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
