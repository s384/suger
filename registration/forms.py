from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TypeUser

class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido, 254 caracteres maximo"
                " y debe ser valido")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ya fue registrado")
        return email

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