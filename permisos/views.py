from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import SolicitudPermisos
from django.contrib.auth.models import User
from .forms import (SolicitudPermisosForm, EstadoSolicitudForm,
    TrabajadorSolicitudForm)


class SolicitudPermisosList(ListView):
    model = SolicitudPermisos

    def get_queryset(self):
        qs = super().get_queryset()
        usuario = User.objects.get(username=self.request.user)
        if usuario.profile.type_user == 1:
            return qs
        elif usuario.profile.type_user == 2:
            qs = qs.filter(usuario__profile__cargo_user__area__boss_user  = usuario)
            return qs
        elif usuario.profile.type_user == 3:
            qs = qs.filter(usuario = self.request.user)
        return qs.exclude(estado_solicitud=4)

class SolicitudPermisosForm(CreateView):
    model = SolicitudPermisos
    form_class = SolicitudPermisosForm
    template_name = 'permisos/solicitudpermisos_form.html'
    success_url = reverse_lazy('SolicitudPermisosList')

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        permisos_form = form.save(commit=False)
        permisos_form.usuario = self.request.user
        permisos_form.save()
        '''
        noti = Notificacion.objects.get_or_create(
        asunto = "Tarea asignada",
        descripcion = form['titulo'].value(),
        usuario = respon,
        prioridad = form['prioridad'].value()
        )
        '''
        return redirect(self.success_url)

class SolicitudPermisosDetail(DetailView):
    model = SolicitudPermisos
    template_name_suffix = '_detail'

class EstadoSolicitudUpdate(UpdateView):
    model = SolicitudPermisos
    form_class = EstadoSolicitudForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('SolicitudPermisosList')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.user = self.object.usuario
            self.inicio = self.object.fecha_inicio
            self.dias = self.object.dias_permiso
        else:
            return self.form_invalid(form)


class EstadoSolicitudUpdateTrabajador(UpdateView):
    model = SolicitudPermisos
    form_class = TrabajadorSolicitudForm
    template_name_suffix = '_update_form_trabajador'
    success_url = reverse_lazy('SolicitudPermisosList')