from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from registration.models import Profile
from django.contrib.auth.models import User
from registration.forms import (UserCreationFormWithEmail,
    ProfileForm, UserActive, UserUpdateForm, ProfileUpdateForm)
from tareas.models import Tareas, SolicitudTarea
# Para el horario
from datetime import timedelta, date, time, datetime
from turnos.models import HorarioUsuario
from permisos.models import SolicitudPermisos


@method_decorator(login_required, name='dispatch')
class UserList(ListView):
    model = User
    template_name = 'registration/user_list.html'
    #paginate_by = 10
    def get_queryset(self):
        qs = super().get_queryset()
        usuario = User.objects.get(username=self.request.user)
        if usuario.profile.type_user == 1:
            return qs
        elif usuario.profile.type_user == 2:
            qs = qs.filter(profile__cargo_user__area__boss_user = usuario)
            return qs


@method_decorator(login_required, name='dispatch')
class UserCreate(CreateView):
    model = User
    template_name = 'registration/user_form.html'
    form_class = UserCreationFormWithEmail

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        user_creation = form.save(commit=False)
        user_creation.is_active = False
        user_creation.save()
        return HttpResponseRedirect(reverse_lazy('newPerfil', kwargs={'pk': user_creation.pk}))

@method_decorator(login_required, name='dispatch')
class UserUpdate(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'registration/user_form.html'

    def get_success_url(self):
        userId=self.kwargs['pk']
        return reverse_lazy('updatePerfil', kwargs={'pk': userId})

@method_decorator(login_required, name='dispatch')
class UserDelete(UpdateView):
    model = User
    form_class = UserActive
    template_name = 'registration/user_confirm_delete.html'
    success_url = reverse_lazy('user')

@method_decorator(login_required, name='dispatch')
class UserDetail(DetailView):
    model = User
    template_name = 'registration/profile_detail.html'



@method_decorator(login_required, name='dispatch')
class ProfileCreate(UpdateView):
    model = Profile
    template_name = 'registration/profile_form.html'
    form_class = ProfileForm
    success_url = reverse_lazy('user')


@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'registration/profile_form.html'
    success_url = reverse_lazy('user')


class ProfileWorkUpdate(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'registration/profile_update.html'
    
    def get_success_url(self):
        userId=self.object.pk
        return reverse_lazy('detailUser', kwargs={'pk': userId})


def home(request):
    if request.user.is_authenticated:
        # Tareas del usuario
        tareas = Tareas.objects.filter(responsable=request.user)[:3]
        # Solicitudes de tareas para el jefe de area
        solicitudes = SolicitudTarea.objects.filter(
            area_destino__boss_user=request.user)[:3]
        # Solicitudes de permisos aprobadas del area
        permisos = SolicitudPermisos.objects.filter(
            estado_solicitud = 4 ).filter(usuario__profile__cargo_user__area =
            request.user.profile.cargo_user.area)[:3]
        # Solicitudes de tareas para el jefe de area
        if request.user.profile.type_user ==2:
            soli_permisos = SolicitudPermisos.objects.filter(
                usuario__profile__cargo_user__area__boss_user=request.user)
            soli_permisos = soli_permisos.exclude(estado_solicitud=4)[:3]
        elif request.user.profile.type_user ==1:
            soli_permisos = SolicitudPermisos.objects.exclude(estado_solicitud=4)[:3]
        else:
            soli_permisos = None

        inicio_semana = datetime.today()-timedelta(days=datetime.today().weekday())
        dias_restantes = 7 - datetime.today().isoweekday() 
        fin_semana = datetime.today()+timedelta(days=dias_restantes)
        #.filter(dia_semana=)
        horario = HorarioUsuario.objects.filter(
            turno_usuario__usuario=request.user).filter(
            dia_semana__range=[inicio_semana, fin_semana])
        context = {
        'tareas':tareas, 
        'solicitudes':solicitudes,
        'horario':horario,
        'permisos':permisos,
        'soli_permisos':soli_permisos,
        }

        return render(request, 'core/index.html', context)
    else:
        return render(request, 'registration/login.html')


def profile(request):
    if request.user.is_authenticated:
        if not request.user.profile.first_login:
            return render(request, 'registration/account_activation_form.html')
        else:
            # Crear index del perfil, para editar datos
            return render(request, 'core/index.html')
    else:
        return render(request, 'registration/login.html')

@login_required
def user(request):
    return render(request, 'core/user.html')

def job(request):
    return render(request, 'core/job.html')

@login_required
def turn(request):
    return render(request, 'core/turn.html')

@login_required
def work(request):
    return render(request, 'core/work.html')