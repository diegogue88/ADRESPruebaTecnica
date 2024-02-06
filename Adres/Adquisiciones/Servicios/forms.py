# En tu archivo forms.py
from django import forms
from .models import Registro

class FiltroRegistrosForm(forms.Form):
    q = forms.CharField(label='Buscar por cualquier campo', required=False)


    tipo_servicio = forms.CharField(label='Tipo de servicio', required=False)
    valor_total_min = forms.DecimalField(label='Valor total mínimo', required=False)
    valor_total_max = forms.DecimalField(label='Valor total máximo', required=False)

    fecha_adquisicion = forms.DateField(label='Fecha de adquisición', required=False)


    proveedor = forms.CharField(label='Proveedor', required=False)

    

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = '__all__'
        widgets = {
            'FechaAdquisicion': forms.DateInput(attrs={'type': 'date'}),
        }