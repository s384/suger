from django.urls import path
from .views import (TareasList,TareasCreate,informe_tareas,
                    SolicitudTareaList,SolicitudTareasCreate,
                    SolicitudTareasDetail, SolicitudRechazada,
                    SolicitudTareasUpdate, TareasUpdateResponsable)
urlpatterns = [
    #Solicitud de tareas
    path('Solicitud-tarea', SolicitudTareaList.as_view(), name="listSolicitudTarea"),
    path('nueva-solicitud', SolicitudTareasCreate.as_view(), name="createSolicitudTarea"),
    path('detalle-solicitud/<slug:slug>', SolicitudTareasDetail.as_view(), name="detailSolicitudTarea"),
    path('update-solicitud/<slug:slug>', SolicitudTareasUpdate.as_view(), name="updateSolicitudTarea"),
    path('rechazar-solicitud/<slug:slug>', SolicitudRechazada.as_view(), name="rechazarSolicitud"),
	#Tareas
    path('', TareasList.as_view(), name="listTareas"),
    path('nueva-tarea/<slug:slug>', TareasCreate.as_view(), name="createTareas"),
    path('actualizar/<int:pk>', TareasUpdateResponsable.as_view(), name="responsableTarea"),
    path('informe-tareas', informe_tareas, name="informeTareas"),
]