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
	def clean_titulo(self):
		titulo = self.cleaned_data.get("titulo")
		if Cargo.objects.filter(titulo=titulo).exists():
			raise forms.ValidationError("Este cargo ya existe dentro del area seleccionada")
		return titulo



