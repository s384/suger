from django import forms
from .models import Cargo

class CargoForm(forms.ModelForm):
	class Meta:
		model = Cargo
		fields = ['area','titulo','descripcion']
		widgets = {
			'area' : forms.Select(attrs={'class' : 'form-control'}),
			'titulo' : forms.TextInput(attrs={'class' : 'form-control'}),
			'descripcion' : forms.Textarea(attrs={'class' : 'form-control', 'cols': 8}),
		}
