from django import forms
from .models import Tareas

class TareasForm(forms.ModelForm):

    class Meta:
        model = Tareas
        fields = ('titulo','supervisor','prioridad','responsable',
                  'descripcion')
        widgets = {
            'titulo' : forms.TextInput(attrs={'class':'form-control'}),
            'prioridad' : forms.Select(attrs={'class':'form-control'}),
            'descripcion' : forms.Textarea(attrs={'class':'form-control', 'cols': 8}),
        }