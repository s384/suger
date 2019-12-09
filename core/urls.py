from django.urls import path
# Importamos las vistas para asignarlas a las urls
from .views import (home, job, turn, work, profile, TypeUserUpdate,
                    TypeUserList, TypeUserCreate, TypeUserDelete,
                    UserList, UserCreate, UserDelete, UserUpdate,
                    UserDetail, ProfileCreate, 
                    AreaList, AreaCreate, AreaDelete, AreaUpdate,
                    SubAreaList, SubAreaCreate, SubAreaUpdate,
                    SubAreaDelete)

# Si la vista es una funcion, solo lleva el nombre de ella,
# cuando es una clase debe ser completada con .as_view()

urlpatterns = [
    # El primer valor es el el que mostrara la url
    # es puede cambiar las veces que quieras sin modificar
    # nada mas.
    # El segundo valor es la vista que se utilizara.
    # El tercero es le nombre que utilizaremos para cargar en los
    # campos <a href=''> de los template
    path('', home, name="home"),
    path('perfil/', profile, name="profile"),
    path('usuarios/', UserList.as_view(), name="user"),
    path('nuevo-usuarios/', UserCreate.as_view(), name="newUser"),
    path('borrar-usuario/<int:pk>/', UserDelete.as_view(), name="deleteUser"),
    path('modificar-usuario/<int:pk>/', UserUpdate.as_view(), name="updateUser"),
    path('detalle-usuario/<int:pk>/', UserDetail.as_view(), name="detailUser"),
    path('nuevo-perfil/', ProfileCreate.as_view(), name="newPerfil"),
    path('areas/', AreaList.as_view(), name="area"),
    path('borrar-area/<int:pk>/', AreaDelete.as_view(), name="deleteArea"),
    path('modificar-area/<int:pk>/', AreaUpdate.as_view(), name="updateArea"),
    path('nueva-area/', AreaCreate.as_view(), name="newArea"),
    #path('tipo-usuario/', TypeUserList.as_view(), name="typeUser"),
    #path('nuevo-tipo-usuario/', TypeUserCreate.as_view(), name="newTypeUser"),
    #path('modificar-tipo-usuario/<int:pk>/', TypeUserUpdate.as_view(), name="updateTypeUser"),
    #path('borrar-tipo-usuario/<int:pk>/', TypeUserDelete.as_view(), name="deleteTypeUser"),
    path('job/', job, name="job"),
    path('turn/', turn, name="turn"),
    path('work/', work, name="work"),
    #sub-áreas
    path('subareas/', SubAreaList.as_view(), name='SubAreas'),
    path('creación-sub-area/', SubAreaCreate.as_view(), name='newSubArea'),
    path('actualizar-sub-area/<int:pk>/', SubAreaUpdate.as_view(), name="updateSubArea"),
    path('borrar-sub-area/<int:pk>/', SubAreaDelete.as_view(), name="deleteSubArea"),

]