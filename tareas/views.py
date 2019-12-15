from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.db.models import Count
from registration.models import Area
from notificaciones.models import Notificacion
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
        self.solicitud = get_object_or_404(SolicitudTarea, slug=slug_solicitud)
        context['solicitud'] = self.solicitud
        responsable = User.objects.filter(profile__type_user=3).filter(
            profile__area_user=self.solicitud.area_destino)
        context['responsable'] = responsable
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            self.user = request.user
            self.responsable = request.POST.get('responsable_2')
            slug_solicitud=self.kwargs['slug']
            self.solicitud = get_object_or_404(SolicitudTarea, slug=slug_solicitud)
            return self.form_valid(form, self.solicitud)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, solicitud):
        tareas_creation = form.save(commit=False)
        #tareas_creation.titulo = form.titulo
        tareas_creation.supervisor = self.user
        if form['area_destino'].value() == "":
            tareas_creation.area_destino = solicitud.area_destino
            respon = get_object_or_404(User, pk=form['responsable'].value())
            tareas_creation.responsable = respon
        elif form['area_destino'].value() != "":
            area = get_object_or_404(Area, pk=form['area_destino'].value())
            tareas_creation.area_destino = area
            respon = get_object_or_404(User, pk=self.responsable)
            tareas_creation.responsable = respon
        
        tareas_creation.save()

        noti = Notificacion.objects.get_or_create(
        asunto = "Tarea asignada",
        descripcion = form['titulo'].value(),
        usuario = respon,
        prioridad = form['prioridad'].value()
            )

        solicitud.estado_solicitud = 4
        solicitud.save()

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

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(estado_solicitud=4)

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
        
        area_soli = get_object_or_404(Area, pk=form['area_destino'].value())
        
        noti = Notificacion.objects.get_or_create(
        asunto = "Solicitud de tarea pendiente",
        descripcion = form['titulo'].value(),
        usuario = area_soli.boss_user,
        prioridad = form['prioridad'].value()
        )

        return redirect(self.success_url)

class SolicitudTareasUpdate(UpdateView):
    model = SolicitudTarea
    form_class = SolicitudTareaForm

class SolicitudTareasDetail(DetailView):
    model = SolicitudTarea
