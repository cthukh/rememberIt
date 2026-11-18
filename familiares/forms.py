from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import Familiar

class IniciarSesionFamiliar(forms.Form):
    rut = forms.CharField(
        label="RUT",
    )
    password = forms.CharField(
        label="Clave",
        widget=forms.PasswordInput(attrs={"autocamplete": "current-password"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class RegistrarFamiliarForm(forms.ModelForm):
    password2 = forms.CharField(
        label="Confirmar clave",
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = Familiar
        fields = (
            'rut',
            'primer_nombre',
            'segundo_nombre',
            'apellido_paterno',
            'apellido_materno',
            'telefono',
            'correo',
            'parentesco',
            'password',
            'password2',   # campo extra, no está en el modelo
        )
        labels = {
            'rut': "RUT",
            'primer_nombre': "Primer nombre",
            'segundo_nombre': "Segundo nombre",
            'apellido_paterno': "Apellido paterno",
            'apellido_materno': "Apellido materno",
            'telefono': "Teléfono contacto",
            'correo': "Correo electrónico",
            'parentesco': "Parentesco con el residente",
            'password': "Clave",
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "form-control")

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('password2')

        if p1 and p2 and p1 != p2:
            self.add_error('password2', "Las claves no coinciden.")

        # Opcional: aplica las reglas de seguridad de Django (largo mínimo, etc.)
        if p1:
            try:
                validate_password(p1)
            except forms.ValidationError as e:
                self.add_error('password', e)

        return cleaned