from django import forms
from registration.models import Area

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre','boss_user']
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'boss_user' : forms.Select(attrs={'class':'form-control'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if Area.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError("Está área ya ha sido creada")
        return nombre


    def clean_boss_user(self):
        boss_user = self.cleaned_data.get("boss_user")
        if Area.objects.filter(boss_user=boss_user).exists():
            raise forms.ValidationError("El usuario seleccionado ya cuenta con jefatura")
        return boss_user

class AreaUpdateForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre','boss_user']
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'boss_user' : forms.Select(attrs={'class':'form-control'}),
        }

    def clean_boss_user(self):
        boss_user = self.cleaned_data.get("boss_user")
        nombre = self.cleaned_data.get("nombre")
        if Area.objects.filter(nombre=nombre).exists():
            if Area.objects.filter(boss_user=boss_user).exists():
                raise forms.ValidationError("El usuario seleccionado ya cuenta con jefatura")

            return boss_user  
        else:
            return boss_user     