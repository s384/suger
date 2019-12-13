from django.urls import path
from .views import (CargoList, CargoCreate, CargoUpdate)

urlpatterns = [
    path('', CargoList.as_view(), name="CargoList"),
    path('crear-cargo/', CargoCreate.as_view(), name="CargoCreate"),
    path('modificar-cargo/<slug:slug>', CargoUpdate.as_view(), name="CargoUpdate"),    
]