from django import forms
from .models import Turnos, DetalleTurnos

class TurnosForm(forms.ModelForm):
	class Meta:
		model = Turnos
		fields = ["nombre","descripcion","area","tipo_turno","fecha_inicio",
		"hora_inicio","duracion_horas","tipo_continuidad","fecha_fin"]
		widgets = {
			'nombre' : forms.TextInput(attrs={'class' : 'form-control'}),
			'descripcion' : forms.Textarea(attrs={'class' : 'form-control', 'cols' : 8}),
			'area' : forms.Select(attrs={'class' : 'form-control'}),
			'duracion_horas' : forms.TextInput(attrs={'class' : 'form-control'}),
			'tipo_turno' : forms.RadioSelect(attrs={'class' : 'radio'}),
			'tipo_continuidad' : forms.RadioSelect(attrs={'class' : 'radio'}),
		}

class DetalleTurnosForm(forms.ModelForm):
	class Meta:
		model = DetalleTurnos
		fields = ["cargo","cantidad"]
		widgets = {
			'cargo' : forms.SelectMultiple(attrs = {'class' : 'form-control'}),
			'cantidad' : forms.NumberInput(attrs = {'class' : 'form-control'}),
		}
