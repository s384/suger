from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from cargos.models import Cargo
from .models import Turnos, DetalleTurnos
from .forms import TurnosForm, DetalleTurnosForm, CargosForm

# Views asociadas a Turnos

@method_decorator(login_required, name='dispatch')
class TurnosList(ListView):
    model = Turnos

@method_decorator(login_required, name='dispatch')
class TurnosCreate(CreateView):
    model = Turnos
    form_class = TurnosForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        tareas_creation = form.save(commit=False)
        tareas_creation.save()
        return HttpResponseRedirect(reverse_lazy('seleccionCargos', kwargs={'pk': tareas_creation.pk}))


@method_decorator(login_required, name='dispatch')
class TurnosUpdate(UpdateView):
    model = Turnos
    form_class = TurnosForm
    success_url = reverse_lazy('TurnosList')

# Views asociadas a DetalleTurnos

@method_decorator(login_required, name='dispatch')
class DetalleTurnosList(ListView):
    model = DetalleTurnos

def CrearDetalleTurnosCicloFor(request, pk):
    turno = Turnos.objects.get(pk=pk)
    cargos = request.POST
    for variable in cargos:
        if variable != 'csrfmiddlewaretoken':
            cargo = Cargo.objects.get(titulo=variable)
            detail_turn = DetalleTurnos(turno=turno,
                cargo=cargo, cantidad=request.POST.get(variable))
            detail_turn.save()

    return HttpResponseRedirect(reverse_lazy('TurnosList'))

def DetalleTurnosCreate(request, pk):
    turno = Turnos.objects.get(pk=pk)
    cargos = request.POST.getlist('cargo')
    cargos = Cargo.objects.filter(pk__in=cargos)
    return render(request, 'turnos/detalleturnos_form.html', 
    {'turno':turno,'cargos': cargos,})

@method_decorator(login_required, name='dispatch')
class DetalleTurnosUpdate(UpdateView):
    model = DetalleTurnos
    form_class = DetalleTurnosForm
    success_url = reverse_lazy('DetalleTurnosList')

def form_cargos(request, pk):
    turno = Turnos.objects.get(pk=pk)
    cargos = Cargo.objects.filter(area=turno.area)
    context = {'turno':turno,'cargos': cargos,}

    return render(request, 'turnos/cargos_form.html', context)