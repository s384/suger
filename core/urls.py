from django.urls import path, include
from .views import (home, user, job, turn, work, TypeUserUpdate,
                    TypeUserList, TypeUserCreate, TypeUserDelete)

urlpatterns = [
    path('', home, name="home"),
    path('user/', user, name="user"),
    path('tipo-usuario/', TypeUserList.as_view(), name="typeUser"),
    path('nuevo-tipo-usuario/', TypeUserCreate.as_view(), name="newTypeUser"),
    path('modificar-tipo-usuario/<int:pk>/', TypeUserUpdate.as_view(), name="updateTypeUser"),
    path('Borrar-tipo-usuario/<int:pk>/', TypeUserDelete.as_view(), name="deleteTypeUser"),
    path('job/', job, name="job"),
    path('turn/', turn, name="turn"),
    path('work/', work, name="work"),
]