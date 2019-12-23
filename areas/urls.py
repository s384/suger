from django.urls import path
from .views import AreaList, AreaCreate, AreaUpdate, AreaDetail

urlpatterns = [
    path('', AreaList.as_view(), name="area"),
    path('modificar-area/<int:pk>/', AreaUpdate.as_view(), name="updateArea"),
    path('nueva-area/', AreaCreate.as_view(), name="newArea"),
    path('detalle-area/<slug:slug>', AreaDetail.as_view(), name="detailArea"),
]