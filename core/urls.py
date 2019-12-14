from django.urls import path
from .views import (home, job, turn, work, profile, TypeUserUpdate,
                    TypeUserList, TypeUserCreate, TypeUserDelete,
                    UserList, UserCreate, UserDelete, UserUpdate,
                    UserDetail, ProfileCreate, ProfileUpdate,
                    AreaList, AreaCreate, AreaDelete, AreaUpdate)
from cargos.views import (CargoList, CargoCreate, CargoUpdate)

urlpatterns = [
    path('', home, name="home"),
    # Perfil
    path('perfil/', profile, name="profile"),
    path('nuevo-perfil/<int:pk>', ProfileCreate.as_view(), name="newPerfil"),
    path('modificar-perfil/<int:pk>', ProfileUpdate.as_view(), name="updatePerfil"),
    # Usuarios
    path('usuarios/', UserList.as_view(), name="user"),
    path('nuevo-usuarios/', UserCreate.as_view(), name="newUser"),
    path('borrar-usuario/<int:pk>/', UserDelete.as_view(), name="deleteUser"),
    path('activar-usuario/<int:pk>/', UserDelete.as_view(), name="activeUser"),
    path('modificar-usuario/<int:pk>/', UserUpdate.as_view(), name="updateUser"),
    path('detalle-usuario/<int:pk>/', UserDetail.as_view(), name="detailUser"),
    # Areas
    path('areas/', AreaList.as_view(), name="area"),
    path('borrar-area/<int:pk>/', AreaDelete.as_view(), name="deleteArea"),
    path('modificar-area/<int:pk>/', AreaUpdate.as_view(), name="updateArea"),
    path('nueva-area/', AreaCreate.as_view(), name="newArea"),
    # Otras
    path('job/', job, name="job"),
    path('turn/', turn, name="turn"),
    path('work/', work, name="work"),
]