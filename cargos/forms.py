from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from registration.models import Area
from cargos.models import Cargo

class CargoForm(forms.ModelForm):
	class meta:
		model = Cargo
		fields = ['area','titulo','descripcion']
		widgets = {
			'area' : forms.Select(attrs={'class' : 'form-control'}),
			'titulo' : forms.TextInput(attrs={'class' : 'form-control'}),
			'descripcion' : forms.Textarea(attrs={'class' : 'form-control', 'cols': 8}),
		}