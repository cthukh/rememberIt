from django import forms
from .models import Recordatorio


class CrearRecordatorioForm(forms.ModelForm):
    class Meta:
        model = Recordatorio
        fields = ("nombre", "descripcion", "frecuencia", "fecha_inicio", "fecha_fin")
        labels = {
            "nombre": "NOMBRE RECORDATORIO",
            "descripcion": "DESCRIPCIÓN RECORDATORIO",
            "frecuencia": "FRECUENCIA",
            "fecha_inicio": "FECHA DE INICIO",
            "fecha_fin": "FECHA DE TÉRMINO (opcional)",
        }
        widgets = {
            "fecha_inicio": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "fecha_fin": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.setdefault(
                "class", "form-select" if name == "frecuencia" else "form-control"
            )

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get("fecha_inicio")
        fin = cleaned.get("fecha_fin")
        frecuencia = cleaned.get("frecuencia")

        if inicio and fin and fin < inicio:
            self.add_error("fecha_fin", "La fecha de término no puede ser anterior al inicio.")

        if frecuencia and frecuencia != "UNA" and not fin:
            self.add_error("fecha_fin", "Para un recordatorio repetitivo debes indicar la fecha de término.")

        return cleaned