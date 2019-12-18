from django.urls import path
from .views import (
	SolicitudPermisosList,
	SolicitudPermisosForm,
	SolicitudPermisosUpdate
)

urlpatterns = [
	#URL's de SolicitudesPermisos
    path('mostrar-solicitudes-permisos/', SolicitudPermisosList.as_view(), name="SolicitudPermisosList"),
    path('agregar-solicitudes-permisos/', SolicitudPermisosForm.as_view(), name="SolicitudPermisosForm"),
    path('modificar-solicitudes-permisos/<int:pk>', SolicitudPermisosUpdate.as_view(), name="SolicitudPermisosUpdate"),
]