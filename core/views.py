# Librerias y moduslos a ser utilizados
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# CCBV de django
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Funcion para slugifaicear los campos
from django.template.defaultfilters import slugify
# Importamos el modelo desde la app registration
from registration.models import TypeUser
# Importamos el formulario desde la app registration
from registration.forms import TypeUserForm

# En las vistas cargamos todos los datos que necesitaremos mostrar
# en las template, en este caso las CCBV hacen todo automaticamente,
# son maravillosas.

# Los template de CCBV deben llevar el nombre del modelo y la funcion
# typeuser_list, typeuser_detail, typeuser_update_form
# el unico que cambia es el delete, ya qu el template es de confirmacion
# typeuser_confirm_delete

class TypeUserList(ListView):
    # Asignamos el modelo a la variable model, como nos dice
    # la doc de CCBV de django ( http://ccbv.co.uk/ )
    model = TypeUser
    # Tambien es posible paginar con
    # paginated_by = 8
    # Esto quiere decir que mostrara 8 registros por pagina

class TypeUserCreate(CreateView):
    # Asignamos el modelo a la variable
    model = TypeUser
    # Cargamos el formulario creado en la app registration
    form_class = TypeUserForm
    # Establecemos la url a la que nos redireccionara cuando
    # termine de crear el objeto
    success_url = reverse_lazy('typeUser')

    # Funcion Post
    def post(self, request, *args, **kwargs):
        # Obtenemos el formulario
        form = self.get_form()
        # Obtenemos el nombre que ingresamos en el formulario
        self.nombre = request.POST.get('nombre')
        # Consultamos si el formulario es valido
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # Funcion formulario valido
    def form_valid(self, form):
        # Creamos un objeto con los datos del formulario. antes de 
        # guardarlo en la db
        typeUser = form.save(commit=False)
        # Creamos el slug del objeto con el nombre obtenido anteriormente
        typeUser.slug = slugify(self.nombre)
        # Grabamos el objeto en la db
        typeUser.save()
        # Si todo esta bien, rediriginos a la url establecida al principio
        return redirect(self.success_url)

class TypeUserUpdate(UpdateView):
    # Asignamos el objeto en la variable
    model = TypeUser
    # Utilizamos el mismo formulario creado en registratios
    form_class = TypeUserForm
    # Asignamos el nombre que tendra el formulario, aparte de typeuser
    template_name_suffix = '_update_form'
    # Asignamos a donde iremos cuando terminemos
    success_url = reverse_lazy('typeUser')

class TypeUserDelete(DeleteView):
    # Asignamos el objeto en la variable
    model = TypeUser
    # Asignamos a donde iremos cuando terminemos
    success_url = reverse_lazy('typeUser')


def home(request):
    return render(request, 'core/index.html')

def user(request):
    return render(request, 'core/user.html')

def job(request):
    return render(request, 'core/job.html')

def turn(request):
    return render(request, 'core/turn.html')

def work(request):
    return render(request, 'core/work.html')