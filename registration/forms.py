from django import forms
from .models import TypeUser

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