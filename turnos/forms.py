from django import forms
from .models import Turnos, DetalleTurnos

class TurnosForm(forms.ModelForm):
	class Meta:
		model = Turnos
		fields = ["nombre","descripcion","area","tipo_turno","fecha_inicio",
		"hora_inicio","duracion_horas","tipo_continuidad","fecha_fin",]
		widgets = {
			'nombre' : forms.TextInput(attrs={'class' : 'form-control'}),
			'descripcion' : forms.Textarea(attrs={'class' : 'form-control', 'cols' : 8}),
			'area' : forms.Select(attrs={'class' : 'form-control'}),
			'tipo_turno' : forms.RadioSelect(attrs={'class' : 'form-control'}),
			'fecha_inicio' : forms.TimeInput(attrs={'class' : 'form-control'}),
			'hora_inicio' : forms.DateInput(attrs={'class' : 'form-control'}),
			'duracion_horas' : forms.TimeInput(attrs={'class' : 'form-control'}),
			'tipo_continuidad' : forms.RadioSelect(attrs={'class' : 'form-control'}),
			'fecha_fin' : forms.DateInput(attrs={'class' : 'form-control'}),
		}

class DetalleTurnosForm(forms.ModelForm):
	class Meta:
		model = DetalleTurnos
		fields = ["cargo","cantidad"]
		widgets = {
			'cargo' : forms.SelectMultiple(attrs = {'class' : 'form-control'}),
			'cantidad' : forms.NumberInput(attrs = {'class' : 'form-control'}),
		}
