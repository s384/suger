# Librerias y moduslos a ser utilizados
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# CCBV de django
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Funcion para slugifaicear los campos
from django.template.defaultfilters import slugify
# Login required para ver las paginas
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Importamos el modelo desde la app registration
from registration.models import TypeUser, Profile, Area, SubArea
from django.contrib.auth.models import User
# Importamos el formulario desde la app registration
from registration.forms import (TypeUserForm, UserCreationFormWithEmail,
    ProfileForm, AreaForm, SubAreaForm)

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
    paginate_by = 10

@method_decorator(login_required, name='dispatch')
class AreaCreate(CreateView):
    model = Area
    template_name = 'registration/area_form.html'
    form_class = AreaForm
    success_url = reverse_lazy('area')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuarios = User.objects.all()
        context['users'] = usuarios
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

@method_decorator(login_required, name='dispatch')
class SubAreaCreate(CreateView):
    model = SubArea
    template_name = 'registration/subareacreate_form.html'
    form_class = SubAreaForm
    success_url = reverse_lazy('SubAreas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuarios = User.objects.all()
        context['users'] = usuarios
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
        usuarios = User.objects.all()
        context['users'] = usuarios
        return context

@method_decorator(login_required, name='dispatch')
class AreaDelete(DeleteView):
    model = Area
    template_name = 'registration/area_confirm_delete.html'
    success_url = reverse_lazy('area')

@method_decorator(login_required, name='dispatch')
class SubAreaList(ListView):
    model = SubArea
    template_name = 'registration/subarea_list.html'
    paginate_by = 10

@method_decorator(login_required, name='dispatch')
class UserList(ListView):
    model = User
    template_name = 'registration/user_list.html'
    paginate_by = 10

@method_decorator(login_required, name='dispatch')
class UserCreate(CreateView):
    model = User
    template_name = 'registration/user_form.html'
    form_class = UserCreationFormWithEmail
    success_url = reverse_lazy('newPerfil')

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form)
            return self.form_invalid(form)

    def form_valid(self, form):
        user_creation = form.save(commit=False)
        user_creation.is_active = True
        user_creation.is_staff = True
        user_creation.is_superuser = True
        user_creation.save()
        return redirect(self.success_url)

@method_decorator(login_required, name='dispatch')
class UserUpdate(UpdateView):
    model = User
    form_class = UserCreationFormWithEmail
    template_name = 'registration/user_form.html'
    success_url = reverse_lazy('user')

@method_decorator(login_required, name='dispatch')
class UserDelete(DeleteView):
    model = User
    template_name = 'registration/user_confirm_delete.html'
    success_url = reverse_lazy('user')


class ProfileCreate(UpdateView):
    template_name = 'registration/profile_form.html'
    form_class = ProfileForm
    success_url = reverse_lazy('user')

    def get_object(self):
        profile = Profile.objects.last()
        return profile


def home(request):
    if request.user.is_authenticated:
        return render(request, 'core/index.html')
    else:
        return render(request, 'registration/login.html')


def profile(request):
    if request.user.is_authenticated:
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