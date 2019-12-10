from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Tareas, SolicitudTarea
from .forms import TareasForm, SolicitudTareaForm
# Create your views here.

#class tareas

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

class TareasUpdate(UpdateView):
    model = Tareas
    form_class = Tareas

def informe_tareas(request):
    cuenta = Tareas.objects.all()
    return render(request, 'tareas/informe_tareas.html', {'cuenta':cuenta})

#class SolicitudTarea

class SolicitudTareaList(ListView):
    model = SolicitudTarea

class SolicitudTareasCreate(CreateView):
    model = SolicitudTarea
    form_class = SolicitudTareaForm
    success_url = reverse_lazy(' ')

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            self.user = request.user
            return self.form_valid(form)
        else:
            print(form)
            return self.form_invalid(form)

    def form_valid(self, form):
        tareas_creation = form.save(commit = False)
        tareas_creation.solicitante = self.user
        tareas_creation.save()

        return redirect(self.success_url)

class SolicitudesTareasUpdate(UpdateView):
    model = SolicitudTarea
    form_class = SolicitudTareaForm

