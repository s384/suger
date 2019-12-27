from django.urls import path
from .views import (
	SolicitudPermisosList,
	SolicitudPermisosForm,
	SolicitudPermisosDetail,
	EstadoSolicitudUpdate,
	EstadoSolicitudUpdateTrabajador,
	SolicitudPermisosListHistorial
)

urlpatterns = [
	#URL's de SolicitudesPermisos
    path('mostrar-permisos/', SolicitudPermisosList.as_view(), name="SolicitudPermisosList"),
    path('mostrar-permisos-historico/', SolicitudPermisosListHistorial.as_view(), name="SolicitudPermisosListHistorial"),
    path('agregar-permisos/', SolicitudPermisosForm.as_view(), name="SolicitudPermisosForm"),
    path('mostrar-permisos-detail/<int:pk>/', SolicitudPermisosDetail.as_view(), name="SolicitudPermisosDetail"),
    path('actualizar-permisos/<int:pk>/', EstadoSolicitudUpdate.as_view(), name="EstadoSolicitudUpdate"),
    path('actualizar-permisos-trabajador/<int:pk>/', EstadoSolicitudUpdateTrabajador.as_view(), name="EstadoSolicitudUpdateTrabajador"),
]