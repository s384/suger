from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template.defaultfilters import slugify
# Importamos el modelo desde la app registration
from registration.models import TypeUser
from registration.forms import TypeUserForm

# Create your views here.

def home(request):
    return render(request, 'core/index.html')

def user(request):
    return render(request, 'core/user.html')

class TypeUserList(ListView):
    model = TypeUser

class TypeUserCreate(CreateView):
    model = TypeUser
    form_class = TypeUserForm
    success_url = reverse_lazy('typeUser')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.nombre = request.POST.get('nombre')
        print(self.nombre)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        typeUser = form.save(commit=False)
        typeUser.slug = slugify(self.nombre)
        typeUser.save()
        return redirect(self.success_url)

class TypeUserDelete(DeleteView):
    model = TypeUser
    success_url = reverse_lazy('typeUser')


def typeUser(request):
    return render(request, 'core/type.html')

def job(request):
    return render(request, 'core/job.html')

def turn(request):
    return render(request, 'core/turn.html')

def work(request):
    return render(request, 'core/work.html')