from django.contrib import admin
from .models import TypeUser

# Register your models here.
class TypeUserAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}
    readonly_fields = ('created', 'updated')

admin.site.register(TypeUser, TypeUserAdmin)