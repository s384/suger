from django import forms
from .models import Tareas, SolicitudTarea

class TareasForm(forms.ModelForm):

	class Meta:
		model = Tareas
		fields = ('titulo','supervisor','prioridad','responsable',
				  'descripcion')
		widgets = {
			'titulo' : forms.TextInput(attrs={'class':'form-control'}),
			'prioridad' : forms.Select(attrs={'class':'form-control'}),
			'descripcion' : forms.Textarea(attrs={'class':'form-control', 'cols': 8}),
		}

class SolicitudTareaForm(forms.ModelForm):
	class Meta:
		model = SolicitudTarea
		fields = ('titulo','area_destino','descripcion','prioridad')
		widgets = {
			'titulo' : forms.TextInput(attrs={'class':'form-control'}),
			'area_destino' : forms.Select(attrs={'class':'form-control'}),
			'descripcion' : forms.Textarea(attrs={'class':'form-control', 'cols': 8}),
			'prioridad' : forms.Select(attrs={'class':'form-control'}),
		}