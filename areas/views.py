from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from registration.models import Area
from cargos.models import Cargo
from django.contrib.auth.models import User
from .forms import AreaForm, AreaUpdateForm

# Create your views here.

@method_decorator(login_required, name='dispatch')
class AreaList(ListView):
    model = Area
    template_name = 'areas/area_list.html'
    #paginate_by = 10

class AreaDetail(DetailView):
    model = Area
    template_name = 'areas/area_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cargos = Cargo.objects.filter(area=self.object)
        context['cargos'] = cargos
        return context

@method_decorator(login_required, name='dispatch')
class AreaCreate(CreateView):
    model = Area
    template_name = 'areas/area_form.html'
    form_class = AreaForm
    success_url = reverse_lazy('area')

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
class AreaUpdate(UpdateView):
    model = Area
    form_class = AreaUpdateForm
    template_name = 'areas/area_update_form.html'
    success_url = reverse_lazy('area')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuarios = User.objects.exclude(profile__type_user=3)
        context['users'] = usuarios
        return context