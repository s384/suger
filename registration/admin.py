from django.contrib import admin
from .models import TypeUser, Area, Profile


class TypeUserAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}
    readonly_fields = ('created', 'updated')

admin.site.register(TypeUser, TypeUserAdmin)
admin.site.register(Area)
admin.site.register(Profile)