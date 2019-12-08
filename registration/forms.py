from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TypeUser, Profile, Area, SubArea

class UserCreationFormWithEmail(UserCreationForm):
	email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ("username","first_name", "last_name", "email", 
				  "password1","password2")
		widgets = {
			'username' : forms.TextInput(attrs={'class':'form-control'}),
			'first_name' : forms.TextInput(attrs={'class':'form-control'}),
			'last_name' : forms.TextInput(attrs={'class':'form-control'}),
		}
		help_texts = {
			'username' : ('Ingrese su rut sin puntos ni guion, con digito verificador.'
						  ' Si su rut termina con K reemplacelo con un 0.'),
		}

	def clean_email(self):
		email = self.cleaned_data.get("email")
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError("El email ya fue registrado")
		return email


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['type_user','area_user']
		widgets = {
			'type_user' : forms.Select(attrs={'class':'form-control'}),
			'area_user' : forms.Select(attrs={'class':'form-control'}),
		}

# Creamos el formulario para ser llamado en el html
class TypeUserForm(forms.ModelForm):
	# Clase meta para obtener los datos necesarios
	class Meta:
		# Asignamos el modelo a la variable model
		model = TypeUser
		# Agregamos el campo nombre del modelo ya que es el unico
		# que sera editable
		fields = ['nombre',]
		# Agregamos el widgets personalizado para que se muestre con 
		# la clase form-control
		widgets = {
			'nombre' : forms.TextInput(attrs={'class':'form-control'}),
		}

class AreaForm(forms.ModelForm):
	class Meta:
		model = Area
		fields = ['nombre','boss_user']
		widgets = {
			'nombre' : forms.TextInput(attrs={'class':'form-control'}),
			'boss_user' : forms.Select(attrs={'class':'form-control'}),
		}

class SubAreaForm(forms.ModelForm):
	class Meta:
		model = SubArea
		fields = ['nombre','area','detalle_subarea']
		widgets = {
			'nombre' : forms.TextInput(attrs={'class': 'form-control'}),
			'area' : forms.Select(attrs={'class':'form-control'}),
			'detalle_subarea' : forms.Textarea(attrs={'class' : 'form-control', 'cols' : 8}),
		}