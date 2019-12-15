from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from cargos.models import Cargo
from .models import Turnos, DetalleTurnos
from .forms import TurnosForm, DetalleTurnosForm

# Views asociadas a Turnos

@method_decorator(login_required, name='dispatch')
class TurnosList(ListView):
	model = Turnos

@method_decorator(login_required, name='dispatch')
class TurnosCreate(CreateView):
	model = Turnos
	form_class = TurnosForm
	success_url = reverse_lazy('Turnos_list')

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			print(form.errors)
			return self.form_invalid(form)

	def form_valid(self, form):
		tareas_creation = form.save(commit=False)
		tareas_creation.save()
		return redirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class TurnosUpdate(UpdateView):
	model = Turnos
	form_class = TurnosForm
	success_url = reverse_lazy('Turnos_list')

# Views asociadas a DetalleTurnos

@method_decorator(login_required, name='dispatch')
class DetalleTurnosList(ListView):
	model = DetalleTurnos

@method_decorator(login_required, name='dispatch')
class DetalleTurnosCreate(CreateView):
	model = DetalleTurnos
	form_class = DetalleTurnosForm
	success_url = reverse_lazy('DetalleTurnos_list')


@method_decorator(login_required, name='dispatch')
class DetalleTurnosUpdate(UpdateView):
	model = DetalleTurnos
	form_class = DetalleTurnosForm
	success_url = reverse_lazy('DetalleTurnos_list')