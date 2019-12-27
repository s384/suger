from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import SolicitudPermisos
from django.contrib.auth.models import User
from registration.models import Area
from .forms import (SolicitudPermisosForm, EstadoSolicitudForm,
    TrabajadorSolicitudForm)
from turnos.models import TurnoUsuario, HorarioUsuario
from notificaciones.models import Notificacion
from datetime import timedelta


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

        noti = Notificacion(
            asunto = "Solicitud de permiso",
            descripcion = form['titulo'].value(),
            usuario = self.request.user.profile.cargo_user.area.boss_user,
            prioridad = 2
        )
        noti.save()

        permisos_form.save()
        return redirect(self.success_url)

class SolicitudPermisosDetail(DetailView):
    model = SolicitudPermisos
    template_name_suffix = '_detail'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.profile.type_user < 3:
            if self.object.estado_solicitud == 1:
                self.object.estado_solicitud = 2
                self.object.save()

                noti = Notificacion(
                    asunto = "Permiso en revision",
                    descripcion = self.object.titulo,
                    usuario = self.object.usuario,
                    prioridad = 1
                    )
                noti.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

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
            self.estado = request.POST.get('estado_solicitud')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        estado_solicitud = form.save(commit=False)
        if self.estado == '4':
            tipo_permiso = self.object.tipo_permiso
            
            if TurnoUsuario.objects.filter(usuario=self.user).exists():
                turno = get_object_or_404(TurnoUsuario, usuario=self.user)
                horario = HorarioUsuario.objects.filter(turno_usuario=turno)
                horario = horario.get(dia_semana=self.inicio)

                dia_inicio = horario.dia_semana
                if tipo_permiso < 2:
                    # Ausencia o permiso administrativo
                    fin_permiso = dia_inicio + timedelta(days=self.dias)
                    i = 0
                    dia = 0
                    while i in range((fin_permiso - dia_inicio).days):
                        dia_ciclo = dia_inicio + timedelta(days=dia)
                        permiso_dia_ciclo = HorarioUsuario.objects.filter(turno_usuario=turno)
                        permiso_dia_ciclo = permiso_dia_ciclo.get(dia_semana=dia_ciclo)
                        if permiso_dia_ciclo.hora_inicio:
                            print(permiso_dia_ciclo.dia_semana)
                            permiso_dia_ciclo.trabajado = tipo_permiso
                            permiso_dia_ciclo.save()
                            i += 1
                        
                        dia += 1
                elif tipo_permiso == 2:
                    # Vacaciones:
                    pass
                elif tipo_permiso == 3:
                    # Licencia
                    fin_permiso = dia_inicio + timedelta(days=self.dias)
                    for i in range((fin_permiso - dia_inicio).days):
                        dia_ciclo = dia_inicio + timedelta(days=i)
                        permiso_dia_ciclo = HorarioUsuario.objects.filter(turno_usuario=turno)
                        permiso_dia_ciclo = permiso_dia_ciclo.get(dia_semana=dia_ciclo)
                        permiso_dia_ciclo.trabajado = tipo_permiso
                        permiso_dia_ciclo.save()
                else:
                    permiso_dia = HorarioUsuario.objects.filter(turno_usuario=turno)
                    permiso_dia = permiso_dia.get(dia_semana=dia_inicio)
                    permiso_dia.trabajado = tipo_permiso
                    permiso_dia.save()
                
                print("Permiso modifico los turnos")

            noti = Notificacion(
                    asunto = "Permiso aprobado",
                    descripcion = self.object.titulo,
                    usuario = self.object.usuario,
                    prioridad = 3
                    )
            noti.save()
        elif self.estado == '3':
            noti = Notificacion(
                    asunto = "Permiso rechazado",
                    descripcion = self.object.titulo,
                    usuario = self.object.usuario,
                    prioridad = 3
                    )
            noti.save()
        print("Terminando todos los if")
        estado_solicitud.save()
        return redirect(self.success_url)


class EstadoSolicitudUpdateTrabajador(UpdateView):
    model = SolicitudPermisos
    form_class = TrabajadorSolicitudForm
    template_name_suffix = '_update_form_trabajador'
    success_url = reverse_lazy('SolicitudPermisosList')