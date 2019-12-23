from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TypeUser, Profile, Area

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


	def clean_first_name(self):
		first_name = self.cleaned_data['first_name']
		if not first_name.isalpha():
			raise forms.ValidationError('El campo Nombre no puede contener números')
		return first_name

	def clean_last_name(self):
		last_name = self.cleaned_data['last_name']
		if not last_name.isalpha():
			raise forms.ValidationError('El campo Apellido no puede contener números')
		return last_name

	def clean_email(self):
		email = self.cleaned_data.get("email")
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError("El email ya fue registrado")
		return email

	


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['type_user','direccion','telefono','cargo_user']
		widgets = {
			'type_user' : forms.Select(attrs={'class':'form-control'}),
			#'area_user' : forms.Select(attrs={'class':'form-control'}),
			'direccion' : forms.TextInput(attrs={'class':'form-control'}),
			'telefono' : forms.TextInput(attrs={'class':'form-control'}),
			'cargo_user' : forms.Select(attrs={'class':'form-control'}),
		}

class TypeUserForm(forms.ModelForm):
	class Meta:
		model = TypeUser
		fields = ['nombre',]
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

class UserActive(forms.ModelForm):
	class Meta:
		model = User
		fields = ['is_active']


class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text="Requerido. 254 carácteres como máximo y debe ser válido.")

    class Meta:
        model = User
        fields = ['email']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        widgets = {
			'username' : forms.TextInput(attrs={'class':'form-control'}),
			'first_name' : forms.TextInput(attrs={'class':'form-control'}),
			'last_name' : forms.TextInput(attrs={'class':'form-control'}),
		}
