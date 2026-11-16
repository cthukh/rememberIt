from django import forms
from .models import Recordatorio

FORMATO_DT = "%Y-%m-%dT%H:%M"


class CrearRecordatorioForm(forms.ModelForm):
    class Meta:
        model = Recordatorio
        fields = ("nombre", "descripcion", "frecuencia", "fecha_inicio", "fecha_fin", "indefinido")
        labels = {
            "nombre": "NOMBRE RECORDATORIO",
            "descripcion": "DESCRIPCIÓN RECORDATORIO",
            "frecuencia": "FRECUENCIA",
            "fecha_inicio": "FECHA DE INICIO",
            "fecha_fin": "FECHA DE TÉRMINO",
            "indefinido": "Repetir indefinidamente (sin fecha de término)",
        }
        widgets = {
            "fecha_inicio": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format=FORMATO_DT
            ),
            "fecha_fin": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format=FORMATO_DT
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fecha_fin"].required = False

        # que el POST también acepte el formato con "T"
        self.fields["fecha_inicio"].input_formats = [FORMATO_DT]
        self.fields["fecha_fin"].input_formats = [FORMATO_DT]

        for name, field in self.fields.items():
            if name == "indefinido":
                clase = "form-check-input"
            elif name == "frecuencia":
                clase = "form-select"
            else:
                clase = "form-control"
            field.widget.attrs.setdefault("class", clase)

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get("fecha_inicio")
        fin = cleaned.get("fecha_fin")
        frecuencia = cleaned.get("frecuencia")
        indefinido = cleaned.get("indefinido")

        if indefinido:
            if frecuencia == "UNA":
                self.add_error("indefinido", "Un recordatorio de una sola vez no puede ser indefinido.")
            cleaned["fecha_fin"] = None  # ignoramos cualquier fecha_fin
            return cleaned

        if inicio and fin and fin < inicio:
            self.add_error("fecha_fin", "La fecha de término no puede ser anterior al inicio.")

        if frecuencia and frecuencia != "UNA" and not fin:
            self.add_error(
                "fecha_fin",
                "Indica la fecha de término o marca 'indefinido'.",
            )

        return cleaned