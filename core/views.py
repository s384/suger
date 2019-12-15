from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from registration.models import TypeUser, Profile, Area
from django.contrib.auth.models import User
from registration.forms import (TypeUserForm, UserCreationFormWithEmail,
    ProfileForm, AreaForm, UserActive, UserUpdateForm)
from tareas.models import Tareas, SolicitudTarea

@method_decorator(login_required, name='dispatch')
class TypeUserList(ListView):
    model = TypeUser
    # paginate_by = 8

@method_decorator(login_required, name='dispatch')
class TypeUserCreate(CreateView):
    model = TypeUser
    form_class = TypeUserForm
    success_url = reverse_lazy('typeUser')


@method_decorator(login_required, name='dispatch')
class TypeUserUpdate(UpdateView):
    model = TypeUser
    form_class = TypeUserForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('typeUser')

@method_decorator(login_required, name='dispatch')
class TypeUserDelete(DeleteView):
    model = TypeUser
    success_url = reverse_lazy('typeUser')



@method_decorator(login_required, name='dispatch')
class AreaList(ListView):
    model = Area
    template_name = 'registration/area_list.html'
    #paginate_by = 10

@method_decorator(login_required, name='dispatch')
class AreaCreate(CreateView):
    model = Area
    template_name = 'registration/area_form.html'
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
    form_class = AreaForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('area')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuarios = User.objects.exclude(profile__type_user=3)
        context['users'] = usuarios
        return context

@method_decorator(login_required, name='dispatch')
class AreaDelete(DeleteView):
    model = Area
    template_name = 'registration/area_confirm_delete.html'
    success_url = reverse_lazy('area')



@method_decorator(login_required, name='dispatch')
class UserList(ListView):
    model = User
    template_name = 'registration/user_list.html'
    #paginate_by = 10

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



def home(request):
    if request.user.is_authenticated:
        tareas = Tareas.objects.filter(responsable=request.user)
        solicitudes = SolicitudTarea.objects.filter(
            area_destino__boss_user=request.user)
        return render(request, 'core/index.html', {
            'tareas':tareas, 'solicitudes':solicitudes,
            })
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

@login_required
def job(request):
    return render(request, 'core/job.html')

@login_required
def turn(request):
    return render(request, 'core/turn.html')

@login_required
def work(request):
    return render(request, 'core/work.html')