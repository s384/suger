from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from registration.models import Area
from .models import Cargo
from .forms import CargoForm


# Create your views here.
@method_decorator(login_required, name='dispatch')
class CargoList(ListView):
    model = Cargo

    def get_queryset(self):
        qs = super().get_queryset()
        # Si el usuario es supervisor, filtramos a su area
        if self.request.user.profile.type_user == 2:
            # Limitamos a las solicitudes que corresponden al area
            qs = qs.filter(area__boss_user=self.request.user)
        # Sacamos las solicitudes ya aprobadas
        return qs

@method_decorator(login_required, name='dispatch')
class CargoDetail(DetailView):
    model = Cargo

@method_decorator(login_required, name='dispatch')
class CargoCreate(CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'cargos/cargo_form.html'
    success_url = reverse_lazy('CargoList')

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

@method_decorator(login_required, name='dispatch')
class CargoUpdate(UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'cargos/cargo_update.html'
    success_url = reverse_lazy('CargoList')

