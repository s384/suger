from django.urls import path
from .views import (TurnosList, TurnosCreate, TurnosUpdate, 
    DetalleTurnosList, DetalleTurnosCreate,	DetalleTurnosUpdate,
    form_cargos, CrearDetalleTurnosCicloFor, AsignarNegrosTurno)
from .generar import generar_horario, validacion_horario

urlpatterns = [
	# URL's de Turnos
    path('mostrar-turnos/', TurnosList.as_view(), name="TurnosList"),
    path('crear-turnos/', TurnosCreate.as_view(), name="TurnosCreate"),
    path('actualizar-turnos/', TurnosUpdate.as_view(), name="TurnosUpdate"),
    # Formulario para seleccionar los cargos
    path('seleccion-cargos/<int:pk>', form_cargos, name="seleccionCargos"),
    # URL's de DetalleTurnos
    path('mostrar-detalle-turnos/', DetalleTurnosList.as_view(), name="DetalleTurnosList"),
    path('crear-detalle-turnos/<int:pk>', DetalleTurnosCreate, name="DetalleTurnosCreate"),
    path('ciclo-for-crear-detalle/<int:pk>', CrearDetalleTurnosCicloFor, name="detailFor"),
    path('actualizar-detalle-turnos/', DetalleTurnosUpdate.as_view(), name="DetalleTurnosUpdate"),
    path('asignar-trabajadores/<int:pk>', AsignarNegrosTurno, name="AsignarNegros"),
    # Generar horarios
    path('horario-generado/<int:pk>', generar_horario, name="generateTimeTable"),
    path('validacion-horario/<int:turno>', validacion_horario, name="validateTimeTable"),
]