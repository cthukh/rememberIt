from django import forms
from .models import Residente

class ResidenteForm(forms.ModelForm):
    class Meta:
        model = Residente
        exclude=['estado']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

        def clean_rut(self):
            rut = self.cleaned_data.get('rut')
            return rut.replace('.', '').replace('-', '').upper()  # Elimina puntos y guiones del RUT
            








        