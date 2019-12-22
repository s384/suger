from django.urls import path
from .views import (
	SolicitudPermisosList,
	SolicitudPermisosForm,
	EstadoSolicitudUpdate,
	EstadoSolicitudUpdateTrabajador
)

urlpatterns = [
	#URL's de SolicitudesPermisos
    path('mostrar-permisos/', SolicitudPermisosList.as_view(), name="SolicitudPermisosList"),
    path('agregar-permisos/', SolicitudPermisosForm.as_view(), name="SolicitudPermisosForm"),
    path('actualizar-permisos/<int:pk>/', EstadoSolicitudUpdate.as_view(), name="EstadoSolicitudUpdate"),
    path('actualizar-permisos-trabajador/<int:pk>', EstadoSolicitudUpdateTrabajador.as_view(), name="EstadoSolicitudUpdateTrabajador"),
]