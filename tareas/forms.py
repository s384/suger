from django import forms
from .models import Tareas, SolicitudTarea

class TareasForm(forms.ModelForm):

	class Meta:
		model = Tareas
		fields = ('titulo','prioridad','responsable',
				  'descripcion', 'area_destino')
		widgets = {
			'titulo' : forms.TextInput(attrs={'class':'form-control'}),
			'prioridad' : forms.Select(attrs={'class':'form-control'}),
			'descripcion' : forms.Textarea(attrs={'class':'form-control', 'cols': 8}),
			'area_destino' : forms.Select(attrs={'class':'form-control'}),
		}

class TareasUpdateResponsableForm(forms.ModelForm):
	class Meta:
		model = Tareas
		fields = ('responsable',)
		widgets = {
			'responsable' : forms.Select(attrs={'class':'form-control'}),
		}

class SolicitudTareaForm(forms.ModelForm):
	class Meta:
		model = SolicitudTarea
		fields = ('titulo','area_destino','descripcion','prioridad','img_referencia')
		widgets = {
			'titulo' : forms.TextInput(attrs={'class':'form-control'}),
			'area_destino' : forms.Select(attrs={'class':'form-control'}),
			'descripcion' : forms.Textarea(attrs={'class':'form-control', 'cols': 8}),
			'prioridad' : forms.Select(attrs={'class':'form-control'}),
			'img_referencia' : forms.FileInput(),
		}

class SolicitudEnRevisionForm(forms.ModelForm):
	class Meta:
		model = SolicitudTarea
		fields = ('estado_solicitud',)
