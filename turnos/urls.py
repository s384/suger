from django.urls import path
from .views import (TurnosList, TurnosCreate, TurnosUpdate, DetalleTurnosList, DetalleTurnosCreate,
	DetalleTurnosUpdate)

urlpatterns = [
	#URL's de Turnos
    path('mostrar-turnos/', TurnosList.as_view(), name="TurnosList"),
    path('crear-turnos/', TurnosCreate.as_view(), name="TurnosCreate"),
    path('actualizar-turnos/', TurnosUpdate.as_view(), name="TurnosUpdate"),
    #URL's de DetalleTurnos
    path('mostrar-DetalleTurnos/', DetalleTurnosList.as_view(), name="DetalleTurnosList"),
    path('crear-DetalleTurnos/', DetalleTurnosCreate.as_view(), name="DetalleTurnosCreate"),
    path('actualizar-DetalleTurnos/', DetalleTurnosUpdate.as_view(), name="DetalleTurnosUpdate"),

]