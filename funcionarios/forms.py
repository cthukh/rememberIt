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


class IniciarSesionFuncionario(forms.Form):
    rut = forms.CharField(
        label="RUT",
        widget=forms.TextInput(attrs={"autocomplete": "username"}),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class PerfilFuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ("phone_number", "rol")
        labels = {
            "phone_number": "Teléfono",
            "rol": "Rol",
        }
        widgets = {
            "phone_number": forms.TextInput(attrs={
                "type": "tel",
                "inputmode": "tel",
                "autocomplete": "tel",
                "class": "form-control",
                "placeholder": "Ingresa tu número de teléfono",
            }),
            "rol": forms.Select(attrs={"class": "form-select"}),
        }