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
from .forms import (TareasForm, SolicitudTareaForm, SolicitudEnRevisionForm,
                    TareasUpdateResponsableForm)

# Create your views here.

class TareasList(ListView):
    model = Tareas

class TareasCreate(CreateView):
    model = Tareas
    form_class = TareasForm
    success_url = reverse_lazy('listTareas')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug_solicitud=self.kwargs['slug']
        self.solicitud = get_object_or_404(SolicitudTarea, slug=slug_solicitud)
        if self.request.user.profile.type_user == 1:
            trabajadores = User.objects.exclude(profile__type_user=1)
            responsable_sol = User.objects.filter(profile__cargo_user__area=self.solicitud.area_destino)
            responsable_sol = responsable_sol.exclude(profile__type_user=1)
        else:
            trabajadores = User.objects.filter(profile__type_user=3)
            responsable_sol = User.objects.filter(profile__cargo_user__area=self.solicitud.area_destino)
            responsable_sol = responsable_sol.filter(profile__type_user=3)
            print(responsable_sol)
        context['responsable_sol'] = responsable_sol
        context['trabajadores'] = trabajadores
        context['solicitud'] = self.solicitud
        responsable = User.objects.filter(profile__type_user=3).filter(
            profile__cargo_user__area=self.solicitud.area_destino)
        context['responsable'] = responsable
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            self.user = request.user
            slug_solicitud=self.kwargs['slug']
            self.solicitud = get_object_or_404(SolicitudTarea, slug=slug_solicitud)
            return self.form_valid(form, self.solicitud)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, solicitud):
        tareas_creation = form.save(commit=False)
        #tareas_creation.titulo = form.titulo
        tareas_creation.supervisor = self.user
        print(solicitud.area_destino)
        tareas_creation.area_destino = solicitud.area_destino
        respon = get_object_or_404(User, pk=form['responsable'].value())
        tareas_creation.responsable = respon
        
        tareas_creation.save()

        noti = Notificacion(
        asunto = "Tarea asignada",
        descripcion = form['titulo'].value(),
        usuario = respon,
        prioridad = form['prioridad'].value()
        )
        noti.save()

        solicitud.estado_solicitud = 4

        noti_2 = Notificacion(
        asunto = "Solicitud aprobada",
        descripcion = solicitud.titulo,
        usuario = solicitud.solicitante,
        prioridad = solicitud.prioridad
        )
        noti_2.save()
        
        solicitud.save()

        return redirect(self.success_url)

class TareasUpdateResponsable(UpdateView):
    model = Tareas
    form_class = TareasUpdateResponsableForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('listTareas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        usuarios = User.objects.filter(profile__cargo_user__area=self.object.area_destino)
        usuarios = usuarios.exclude(profile__type_user=1)
        
        context['usuarios'] = usuarios
        return context


def informe_tareas(request):
    cuenta = Tareas.objects.all()
    return render(request, 'tareas/informe_tareas.html', {'cuenta':cuenta})

#class SolicitudTarea

class SolicitudTareaList(ListView):
    model = SolicitudTarea

    def get_queryset(self):
        qs = super().get_queryset()
        # Si el usuario es supervisor, filtramos a su area
        if self.request.user.profile.type_user == 2:
            # Limitamos a las solicitudes que corresponden al area
            qs = qs.filter(area_destino__boss_user=self.request.user)
        # Sacamos las solicitudes ya aprobadas
        qs = qs.exclude(estado_solicitud=4)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mis_solicitud = SolicitudTarea.objects.filter(solicitante=self.request.user)
        context['mis_solicitud'] = mis_solicitud
        return context

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
        
        noti = Notificacion(
        asunto = "Solicitud de tarea pendiente",
        descripcion = form['titulo'].value(),
        usuario = area_soli.boss_user,
        prioridad = form['prioridad'].value()
        )
        noti.save()

        return redirect(self.success_url)

class SolicitudTareasUpdate(UpdateView):
    model = SolicitudTarea
    form_class = SolicitudTareaForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('listSolicitudTarea')

class SolicitudTareasDetail(DetailView):
    model = SolicitudTarea

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.profile.type_user < 3:
            if self.object.estado_solicitud == 1:
                self.object.estado_solicitud = 2
                self.object.save()

                noti = Notificacion(
                    asunto = "Solicitud de tarea en revision",
                    descripcion = self.object.titulo,
                    usuario = self.object.solicitante,
                    prioridad = self.object.prioridad
                    )
                noti.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class SolicitudRechazada(UpdateView):
    model = SolicitudTarea
    form_class = SolicitudEnRevisionForm
    template_name = "tareas/solicitudtarea_rechazada.html"

    def get_success_url(self):
        return reverse_lazy('detailSolicitudTarea', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        noti = Notificacion(
        asunto = "Solicitud rechazada",
        descripcion = self.object.titulo,
        usuario = self.object.solicitante,
        prioridad = self.object.prioridad
        )
        noti.save()
        return super().post(request, *args, **kwargs)