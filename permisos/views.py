from django.shortcuts import render
from django.urls import reverse_lazy
from django.dispatch import receiver
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Count
from notificaciones.models import Notificacion
from .models import SolicitudPermisos
from .forms import SolicitudPermisosForm


class SolicitudPermisosList(ListView):
    model = SolicitudPermisos

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

class SolicitudPermisosUpdate(UpdateView):
    model = SolicitudPermisos
    form_class = SolicitudPermisosForm
    template_name = 'permisos/solicitudpermisos_update.html'
    success_url = reverse_lazy('SolicitudPermisosList')