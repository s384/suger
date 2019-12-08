from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Tareas
from .forms import TareasForm
# Create your views here.

class TareasList(ListView):
    model = Tareas

class TareasCreate(CreateView):
    model = Tareas
    form_class = TareasForm
    success_url = reverse_lazy('listTareas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supervisor = User.objects.filter(profile__type_user=1)
        context['users'] = supervisor
        responsable = User.objects.exclude(profile__type_user=1)
        context['responsable'] = responsable
        return context

def informe_tareas(request):
    cuenta = Tareas.objects.all()
    return render(request, 'tareas/informe_tareas.html', {'cuenta':cuenta})