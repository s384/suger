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

@method_decorator(login_required, name='dispatch')
class CargoList(ListView):
    model = Cargo
    template_name = 'cargos/cargos_list.html'

@method_decorator(login_required, name='dispatch')
class CargoCreate(CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'cargos/cargos_form.html'
    success_url = reverse_lazy('cargos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuarios = User.objects.exclude(profile__type_user=3)
        context['users_list'] = usuarios
        return context

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
    template_name = 'cargos/cargos_update.html'
    success_url = reverse_lazy('cargos')

# Create your views here.
