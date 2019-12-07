from django.urls import path
from .views import TareasList, TareasCreate, informe_tareas

urlpatterns = [
    path('', TareasList.as_view(), name="listTareas"),
    path('nueva-tarea/', TareasCreate.as_view(), name="createTareas"),
    path('informe-tareas', informe_tareas, name="informeTareas"),
]