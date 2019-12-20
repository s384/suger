from .models import Turnos, DetalleTurnos

def generar_horario(request, turno):
    turno_obtenido = Turnos.objects.get(pk=turno)
    print(turno_obtenido)
    pass