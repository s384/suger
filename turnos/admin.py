from django.contrib import admin
from .models import Turnos, DetalleTurnos, TurnoUsuario, HorarioUsuario

# Register your models here.
admin.site.register(Turnos)
admin.site.register(DetalleTurnos)
admin.site.register(TurnoUsuario)
admin.site.register(HorarioUsuario)