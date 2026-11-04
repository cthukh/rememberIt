from django import forms
from funcionarios.models import Funcionario 
from residentes.models import Residente
from django.contrib.auth.forms import UserCreationForm


class CrearFuncionarioForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model= Funcionario
        fields =('rut','first_name','last_name','email', 'rol')
        labels = {
            "rut": "RUT",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo electrónico",
            "rol": "Rol",
        }

class ActualizarFuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ("rut", "first_name", "last_name", "email", "phone_number", "rol")
        labels = {
            "rut": "RUT",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo electrónico",
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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.setdefault(
                "class", "form-select" if name == "rol" else "form-control"
            )

class CrearResidenteForm(forms.ModelForm):
    class Meta:
        model = Residente
        fields = ("rut","primer_nombre","segundo_nombre","apellido_paterno","apellido_materno","edad","alergias","telefono_emergencias","funcionario","familiar")
        labels = {
            "rut": "RUT",
            "primer_nombre": "Primer nombre",
            "segundo_nombre": "Segundo nombre",
            "apellido_paterno": "Apellido paterno",
            "apellido_materno": "Apellido materno",
            "edad": "Edad",
            "alergias": "Alergias",
            "telefono_emergencias": "Teléfono de emergencias",
            "funcionario": "Funcionario",
            "familiar": "Familiar"
        }
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for name, field in self.fields.items():
                field.widget.attrs.setdefault(
                    "class", "form-select" if name == "rol" else "form-control"
                )