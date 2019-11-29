from django.contrib import admin
from .models import TypeUser

# En este archivo se registran los modelos para
# que sean mostrados en el administrador de django

# Register your models here.
class TypeUserAdmin(admin.ModelAdmin):
    # Funcion para auto poblar un campo
    prepopulated_fields = {'slug': ('nombre',)}
    # Campos que seran de solo lectura
    readonly_fields = ('created', 'updated')

# Registramos el modelo y la clase para que se
# visualize en el admin
admin.site.register(TypeUser, TypeUserAdmin)