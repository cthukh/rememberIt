from django import forms
from .models import Residente
from django.contrib.auth.forms import UserCreationForm

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