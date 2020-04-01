from django import forms
from .models import Skeittispotti

class SpottiForm(forms.ModelForm):
    class Meta:
        model = Skeittispotti
        fields = ['Nimi', 'Kaupunginosa', 'Sijainti']
        widgets = {
            'Nimi' : forms.TextInput(
                attrs={'class':'form-control'}
            ),
            'Kaupunginosa' : forms.TextInput(
                attrs={'class':'form-control'}
            ),
            'Sijainti' : forms.TextInput(
                attrs={'class':'form-control'}
            )
        }