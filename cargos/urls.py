from django.urls import path
from .views import (CargoList, CargoCreate, CargoUpdate,
                    CargoDetail)

urlpatterns = [
    path('', CargoList.as_view(), name="CargoList"),
    path('crear-cargo/', CargoCreate.as_view(), name="CargoCreate"),
    path('modificar-cargo/<int:pk>', CargoUpdate.as_view(), name="CargoUpdate"),    
    path('detalle-cargo/<int:pk>', CargoDetail.as_view(), name="CargoDetail")
]