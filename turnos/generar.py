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
		print("Turno de lunes a viernes, opcion 0")
		# Lunes a viernes
		turno_dias = 0
		duracion_horas = timedelta(hours=10,minutes=0)
	elif turno_obtenido.duracion_horas == 1:
		# Lunes a sabado parejo
		print("Turno de lunes a sabado, opcion 1")
		turno_dias = 1
		duracion_horas = timedelta(hours=8,minutes=30)
	elif turno_obtenido.duracion_horas == 2:
		print("Turno de lunes a sabado, opcion 2")
		# Lunes a viernes 8 horas, sabado 5 horas
		turno_dias = 2
		duracion_horas = timedelta(hours=9,minutes=0)
		duracion_sabado = timedelta(hours=5,minutes=0)

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
			
	# Si el turno es fijo, establecemos la hora de fin
	if not rotacion:
		hora_fin = (datetime.combine(date.today(), hora_inicio) +
				duracion_horas).time()

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

			for i in range((fecha_fin - fecha_inicio).days + 1):
				dia_ciclo = fecha_inicio + timedelta(days=i)

				# Si rotacion es verdadero, hacer calculo horario
				print("El turno comienza a las {}".format(hora_inicio))
				if rotacion:
					if dia_ciclo.weekday() == 0:
						print("Rotacion de turno el dia {}".format(dia_ciclo))
						hora_inicio = (datetime.combine(date.today(), hora_inicio) +
								duracion_horas).time()

				'''
				if turno_dias == 0:
					if dia_ciclo.weekday() in range(0,5):
						# Lunes a viernes
						hora_inicio_guardada = hora_inicio
						hora_fin_guardada = hora_fin
					else:
						hora_inicio_guardada = None
						hora_fin_guardada = None

					guardar_turno(turno_usuario, dia_ciclo,
							hora_inicio_guardada, hora_fin_guardada)

				elif turno_dias == 1:
					if dia_ciclo.weekday() in range(0,6):
						# El rango es de 0 a 5 (Lunes a sabado)
						# Lunes a sabado 7.5 horas
						hora_inicio_guardada = hora_inicio
						hora_fin_guardada = hora_fin
					else:
						hora_inicio_guardada = None
						hora_fin_guardada = None

					guardar_turno(turno_usuario, dia_ciclo,
							hora_inicio_guardada, hora_fin_guardada)

				elif turno_dias == 2:
					if dia_ciclo.weekday() in range(0,5):
						# El rango es de 0 a 4 (Lunes a viernes)
						# Lunes a viernes 8 horas
						hora_inicio_guardada = hora_inicio
						hora_fin_guardada = hora_fin
					elif dia_ciclo.weekday() == 5:
						# Sabado.weekday = 5
						# Sabado 5 horas
						hora_inicio_guardada = hora_inicio
						hora_fin_guardada = (datetime.combine(date.today(), 
								hora_inicio) + duracion_sabado).time()
					else:
						hora_inicio_guardada = None
						hora_fin_guardada = None

					guardar_turno(turno_usuario, dia_ciclo,
							hora_inicio_guardada, hora_fin_guardada)
				'''
	return render(request, 'turnos/horario_generado.html', {'turno':turno_obtenido})
		

def guardar_turno(turno, dia, inicio, fin):
	horario = HorarioUsuario(
		turno_usuario = turno,
		dia_semana = dia,
		hora_inicio = inicio,
		hora_fin = fin,
	)
	horario.save()