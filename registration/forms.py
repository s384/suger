from django import forms
from .models import TypeUser

class TypeUserForm(forms.ModelForm):

    class Meta:
        model = TypeUser
        fields = ['nombre',]
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
        }