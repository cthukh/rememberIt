from django import forms
from .models import Residente
from django.contrib.auth.forms import UserCreationForm


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

class ActuaResidenteForm(forms.ModelForm):
    class Meta:
        model = Residente
        fields = ("alergias", "telefono_emergencias","funcionario","familiar")
        labels = {
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