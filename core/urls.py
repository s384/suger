from django.urls import path, include
from .views import home, user, typeUser, job, turn, work

urlpatterns = [
    path('', home, name="home"),
    path('user/', user, name="user"),
    path('type/', typeUser, name="typeUser"),
    path('job/', job, name="job"),
    path('turn/', turn, name="turn"),
    path('work/', work, name="work"),
]