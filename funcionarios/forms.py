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
        fields =('rut','first_name','last_name','email','username')


class IniciarSesionFuncionario(forms.Form):
    identificador = forms.CharField(
        label="Correo electrónico o RUT",
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


class ActuaFuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ("rut", "first_name", "last_name", "email", "phone_number")
        labels = {
            "rut": "RUT",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo electrónico",
            "phone_number": "Teléfono",
        }
        widgets = {
            "phone_number": forms.TextInput(attrs={
                "type": "tel",
                "inputmode": "tel",
                "autocomplete": "tel",
                "class": "form-control",
                "placeholder": "Ingresa tu número de teléfono",
            }),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.setdefault(
                "class", "form-select" if name == "rol" else "form-control"
            )


class ActuaFuncionarioFormAdmin(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ("rut", "first_name", "last_name", "email", "phone_number", "rol","is_active")
        labels = {
            "rut": "RUT",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo electrónico",
            "phone_number": "Teléfono",
            "rol": "Rol",
            "is_active":"Is_active"
        }
        widgets = {
            "phone_number": forms.TextInput(attrs={
                "type": "tel",
                "inputmode": "tel",
                "autocomplete": "tel",
                "class": "form-control",
                "placeholder": "Ingresa tu número de teléfono",
            }),
            "is_active": forms.CheckboxInput(attrs={
                 "class": "form-check-input"
            }),

            "rol": forms.Select(attrs={"class": "form-select"}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.setdefault(
                "class", "form-select" if name == "rol" else "form-control"
            )