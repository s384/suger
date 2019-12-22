from django import forms
from .models import SolicitudPermisos

class SolicitudPermisosForm(forms.ModelForm):
	class Meta:
		model = SolicitudPermisos
		fields = [
			'titulo',
			'comentario',
			'tipo_permiso',
			'fecha_inicio',
			'dias_permiso',
			'horas_permiso',
			'img_referencia'
		]
		widgets = {
			'titulo' : forms.TextInput(attrs={'class' : 'form-control'}),
			'comentario' : forms.Textarea(attrs={'class' : 'form-control', 'cols' : 8}),
			'tipo_permiso' : forms.Select(attrs={'class' : 'form-control'}),
			'dias_permiso' : forms.NumberInput(attrs={'class' : 'form-control'}),
			'horas_permiso' :forms.NumberInput(attrs={'class' : 'form-control'}),
			'img_referencia' : forms.FileInput(),
		}


class EstadoSolicitudForm(forms.ModelForm):
	class Meta:
		model = SolicitudPermisos
		fields = ['estado_solicitud',]
		widgets = {
			'estado_solicitud' : forms.Select(attrs={'class' : 'form-control'}),
		}

class TrabajadorSolicitudForm(forms.ModelForm):
	class Meta:
		model = SolicitudPermisos
		fields = ['titulo','comentario','tipo_permiso',
			'fecha_inicio',	'dias_permiso',	'horas_permiso',
			'img_referencia']
		widgets = {
			'titulo' : forms.TextInput(attrs={'class' : 'form-control'}),
			'comentario' : forms.Textarea(attrs={'class' : 'form-control', 'cols' : 8}),
			'tipo_permiso' : forms.Select(attrs={'class' : 'form-control'}),
			'dias_permiso' : forms.NumberInput(attrs={'class' : 'form-control'}),
			'horas_permiso' :forms.NumberInput(attrs={'class' : 'form-control'}),
			'img_referencia' : forms.FileInput(),
		}