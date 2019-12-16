from django import forms
from .models import SolicitudPermisos

class SolicitudPermisosForm(forms.ModelForm):
	class Meta:
		model = SolicitudPermisos
		fields = [
			'titulo',
			'comentario',
			'tipo_permiso',
			'tipo_jornada',
			'fecha_inicio',
			'dias_permiso',
			'horas_permiso',
			'img_referencia'
		]
		widgets = {
			'comentario' : forms.Textarea(attrs={'class' : 'form-control', 'cols' : 8}),
			'tipo_permiso' : forms.Select(attrs={'class' : 'form-control'}),
			'tipo_jornada' : forms.Select(attrs={'class' : 'form-control'}),
			'dias_permiso' : forms.NumberInput(attrs={'class' : 'form-control'}),
			'horas_permiso' :forms.NumberInput(attrs={'class' : 'form-control'}),
			'img_referencia' : forms.FileInput(),
		}