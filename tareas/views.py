from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
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
        trabajadores = User.objects.filter(profile__type_user=3)
        context['trabajadores'] = trabajadores
        slug_solicitud=self.kwargs['slug']
        solicitud = get_object_or_404(SolicitudTarea, slug=slug_solicitud)
        context['solicitud'] = solicitud
        responsable = User.objects.filter(profile__type_user=3).filter(
            profile__area_user=solicitud.area_destino)
        context['responsable'] = responsable
        return context

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
        tareas_creation.estado_solicitud = 1
        tareas_creation.save()

        return redirect(self.success_url)

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
    template_name = "tareas/solicitudtarea_form.html"
    success_url = reverse_lazy('listSolicitudTarea')

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
        solicitud_creation = form.save(commit = False)
        solicitud_creation.solicitante = self.user
        solicitud_creation.estado_solicitud = 1
        solicitud_creation.save()

        return redirect(self.success_url)

class SolicitudTareasUpdate(UpdateView):
    model = SolicitudTarea
    form_class = SolicitudTareaForm

class SolicitudTareasDetail(DetailView):
    model = SolicitudTarea
