from django.urls import path
from .views import (TareasList,TareasCreate,informe_tareas,
                    SolicitudTareaList,SolicitudTareasCreate,
                    SolicitudTareasDetail)
urlpatterns = [
    #Solicitud de tareas
    path('Solicitud-tarea', SolicitudTareaList.as_view(), name="listSolicitudTarea"),
    path('nueva-solicitud', SolicitudTareasCreate.as_view(), name="createSolicitudTarea"),
    path('detalle-solicitud/<slug:slug>', SolicitudTareasDetail.as_view(), name="detailSolicitudTarea"),
	#Tareas
    path('', TareasList.as_view(), name="listTareas"),
    path('nueva-tarea/<slug:slug>', TareasCreate.as_view(), name="createTareas"),
    path('informe-tareas', informe_tareas, name="informeTareas"),

]