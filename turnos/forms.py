from django import forms
from .models import Turnos, DetalleTurnos
from cargos.models import Cargo

class TurnosForm(forms.ModelForm):
	class Meta:
		model = Turnos
		fields = ["nombre","descripcion","area","tipo_turno","fecha_inicio",
		"hora_inicio","duracion_horas","fecha_fin"]
		widgets = {
			'nombre' : forms.TextInput(attrs={'class' : 'form-control'}),
			'descripcion' : forms.Textarea(attrs={'class' : 'form-control', 'cols' : 8}),
			'area' : forms.Select(attrs={'class' : 'form-control'}),
			'duracion_horas' : forms.Select(attrs={'class' : 'form-control'}),
			'tipo_turno' : forms.RadioSelect(attrs={'class' : 'radio'}),
		}
		help_texts = {
			'duracion_horas' : ('Lunes a Viernes de 08:00-18:00, '
				'Lunes a Sabado de 08:00-16:30, '
				'Lunes a Viernes 08:00-17:00 / Sabado 08:00-13:00')
		}

class DetalleTurnosForm(forms.ModelForm):
	class Meta:
		model = DetalleTurnos
		fields = ["cargo","cantidad"]
		widgets = {
			'cargo' : forms.SelectMultiple(attrs = {'class' : 'form-control',
					  'style':'height:300px'}),
			'cantidad' : forms.NumberInput(attrs = {'class' : 'form-control'}),
		}

class CargosForm(forms.ModelForm):
	class Meta:
		model = Cargo
		fields = ['titulo']
		widgets = {
			'titulo' : forms.SelectMultiple(attrs = {'class' : 'form-control'})
		}