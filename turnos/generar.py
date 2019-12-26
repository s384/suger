from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from datetime import timedelta, date, time, datetime
# Modelo de usarios
from django.contrib.auth.models import User
# Modelos turnos
from .models import Turnos, DetalleTurnos, TurnoUsuario, HorarioUsuario

def ver_horario(request, pk):
	turno_obtenido = Turnos.objects.get(pk=pk)
	return render(request, 'turnos/horario_generado.html', {'turno':turno_obtenido})

def generar_horario(request, pk):
	turno_obtenido = Turnos.objects.get(pk=pk)
	detalle = DetalleTurnos.objects.filter(turno=turno_obtenido)
	fecha_inicio = turno_obtenido.fecha_inicio
	rotacion = turno_obtenido.tipo_turno

	
	# Obtenemos el tipo de turno y le asignamos la cantidad de horas a utilizar
	if turno_obtenido.duracion_horas == 0:
		# Lunes a viernes
		turno_dias = 0
		duracion_horas = timedelta(hours=10,minutes=0)
	elif turno_obtenido.duracion_horas == 1:
		# Lunes a sabado parejo
		turno_dias = 1
		duracion_horas = timedelta(hours=8,minutes=30)
	elif turno_obtenido.duracion_horas == 2:
		# Lunes a viernes 8 horas, sabado 5 horas
		turno_dias = 2
		duracion_horas = timedelta(hours=9,minutes=0)
		duracion_sabado = timedelta(hours=5,minutes=0)

	# Si el turno tiene fecha de fin
	if turno_obtenido.fecha_fin:
		fecha_fin = turno_obtenido.fecha_fin
	# Si no es el caso, utilizamos el ultimo dia del año
	else:
		fecha_fin = date(date.today().year, 12, 31)
	
	# Por cada detalle del turno generamos un ciclo,
	# esto corresponde a cada cargo 
	for detail in detalle:
		# Filtramos por tipo de usuario (trabajador)
		usuario_obtenido = User.objects.filter(profile__type_user=3)
		# Obtenemos los usuarios del cargo
		usuario_obtenido = usuario_obtenido.filter(profile__cargo_user=detail.cargo.pk)
		# Sacamos aquellos que no tengan activa la cuenta
		usuario_obtenido = usuario_obtenido.exclude(is_active=0)
		# Sacamos los usuarios con turno
		usuario_obtenido = usuario_obtenido.exclude(usuario_turno__usuario__in=usuario_obtenido)

		if usuario_obtenido.count() >= detail.cantidad:
			usuario_azar = usuario_obtenido.order_by('?')[:detail.cantidad]
			for usuario_guardar in usuario_azar:
				# Reiniciamos la hora inicio para el siguiente usuario
				hora_inicio = turno_obtenido.hora_inicio
				# Guardamos el turno_usuario

				turno_usuario = TurnoUsuario(turno=turno_obtenido,
						usuario=usuario_guardar)
				turno_usuario.save()

				# Creamos un contador para consultar la rotacion
				contador = 0
				# Recorremos el rango de fechas
				for i in range((fecha_fin - fecha_inicio).days + 1):
					dia_ciclo = fecha_inicio + timedelta(days=i)

					#print("El turno comienza a las {}".format(hora_inicio))
					
					# Si rotacion es verdadero, hacer calculo horario
					if rotacion:
						# Para el turno numero 3, en opcion rotativa, el turno de 
						# noche es de lunes a viernes, no trabajan el sabado medio dia

						# Dia de la semana = a domingo
						if dia_ciclo.weekday() == 0:
							# Si es el segundo cambio
							if contador % 2:
								hora_inicio = turno_obtenido.hora_inicio
								hora_inicio = (datetime.combine(date.today(), hora_inicio) +
										duracion_horas + timedelta(minutes=30)).time()
							else:
								hora_inicio = turno_obtenido.hora_inicio
							
							contador += 1

					hora_fin = (datetime.combine(date.today(), hora_inicio) +
								duracion_horas).time()


					if turno_dias == 0:
						if dia_ciclo.weekday() in range(0,5):
							# Lunes a viernes
							hora_inicio_guardada = hora_inicio
							hora_fin_guardada = hora_fin
						else:
							hora_inicio_guardada = None
							hora_fin_guardada = None


					elif turno_dias == 1:
						if not (contador-1) % 2:
							if dia_ciclo.weekday() in range(0,6):
								# El rango es de 0 a 5 (Lunes a sabado)
								# Lunes a sabado 7.5 horas
								hora_inicio_guardada = hora_inicio
								hora_fin_guardada = hora_fin
							else:
								hora_inicio_guardada = None
								hora_fin_guardada = None
						else:
							# Turno de noche
							if dia_ciclo.weekday() in range(0,5):
								# Lunes a viernes
								hora_inicio_guardada = hora_inicio
								hora_fin_guardada = hora_fin
							else:
								hora_inicio_guardada = None
								hora_fin_guardada = None


					elif turno_dias == 2:
						if not (contador-1) % 2:
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
						else:
							if dia_ciclo.weekday() in range(0,5):
								# Lunes a viernes
								hora_inicio_guardada = hora_inicio
								hora_fin_guardada = hora_fin
							else:
								hora_inicio_guardada = None
								hora_fin_guardada = None


					guardar_turno(turno_usuario, dia_ciclo,
							hora_inicio_guardada, hora_fin_guardada)
					
	return redirect('detailTimeTable', turno_obtenido.pk)


def guardar_turno(turno, dia, inicio, fin):
	horario = HorarioUsuario(
		turno_usuario = turno,
		dia_semana = dia,
		hora_inicio = inicio,
		hora_fin = fin,
	)
	horario.save()


def validacion_horario(request, turno):
	turno_obtenido = Turnos.objects.get(pk=turno)
	detalle = DetalleTurnos.objects.filter(turno=turno_obtenido)
	validacion = 1
	for detail in detalle:
		# Filtramos por tipo de usuario (trabajador)
		usuario_obtenido = User.objects.filter(profile__type_user=3)
		# Obtenemos los usuarios del cargo
		usuario_obtenido = usuario_obtenido.filter(profile__cargo_user=detail.cargo.pk)
		# Sacamos aquellos que no tengan activa la cuenta
		usuario_obtenido = usuario_obtenido.exclude(is_active=0)
		# Sacamos los usuarios con turno
		usuario_obtenido = usuario_obtenido.exclude(usuario_turno__usuario__in=usuario_obtenido)

		print(usuario_obtenido)
		if usuario_obtenido.count() < detail.cantidad:
			# Si algun cargo no cumple con los requisitos
			# rompeemos el ciclo for
			validacion = 0
			break


	context = {
	'turno':turno_obtenido, 'detalle':detalle,
	'validacion': validacion
	}

	return render(request, 'turnos/validacion_horario.html', context)
	