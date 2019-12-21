from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from datetime import timedelta, date, time, datetime
# Modelo de usarios
from django.contrib.auth.models import User
# Modelos turnos
from .models import Turnos, DetalleTurnos, TurnoUsuario, HorarioUsuario

def generar_horario(request, pk):
    turno_obtenido = Turnos.objects.get(pk=pk)
    detalle = DetalleTurnos.objects.filter(turno=turno_obtenido)
    fecha_inicio = turno_obtenido.fecha_inicio
    rotacion = turno_obtenido.tipo_turno
    hora_inicio = turno_obtenido.hora_inicio
    
    if turno_obtenido.duracion_horas == 0:
        duracion_horas = timedelta(hours=9,minutes=0)
    elif turno_obtenido.duracion_horas == 1:
        duracion_horas = timedelta(hours=8,minutes=0)
        duracion_sabado = timedelta(hours=5,minutes=0)
    elif turno_obtenido.duracion_horas == 2:
        duracion_horas = timedelta(hours=5,minutes=0)

    print("Datos del turno: {}".format(turno_obtenido))
    print("Inicio del turno: {}".format(fecha_inicio.strftime("%w %d/%m/%Y")))

    # Si el turno tiene fecha de fin
    if turno_obtenido.fecha_fin:
        fecha_fin = turno_obtenido.fecha_fin
    # Si no es el caso, utilizamos el ultimo dia del año
    else:
        fecha_fin = date(date.today().year, 12, 31)
    
    print("Fecha de fin: {}".format(fecha_fin.strftime("%w %d/%m/%Y")))
    dias_turno = fecha_fin - fecha_inicio
    print("Duracion del turno: {}".format(dias_turno))

    for detail in detalle:
        print("Cargo seleccionado {}".format(detail.cargo.titulo))
        usuario_obtenido = User.objects.filter(profile__cargo_user=detail.cargo.pk)
        usuario_azar = usuario_obtenido.order_by('?')[:detail.cantidad]
        print("usuarios seleccionado {}".format(usuario_azar))
        # Guardamos los usuarios al modelo turnousuario
        for usuario_guardar in usuario_azar:
            turno_usuario = TurnoUsuario(turno=turno_obtenido,
                usuario=usuario_guardar)
            turno_usuario.save()
            
            # Si rotacion es verdadero, hacer calculo horario
            if rotacion:
                pass
            else:
                hora_fin = (datetime.combine(date.today(), hora_inicio) +
                    duracion_horas).time()
                print(hora_fin)
            
            for i in range((fecha_fin - fecha_inicio).days + 1):
                dia_ciclo = fecha_inicio + timedelta(days=i)
                horario = HorarioUsuario(
                    turno_usuario = turno_usuario,
                    dia_semana = dia_ciclo,
                    hora_inicio = hora_inicio,
                    hora_fin = hora_fin,
                )
                horario.save()


    return render(request, 'turnos/horario_generado.html')
    