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
from registration.models import TypeUser
from django.contrib.auth.models import User
# Importamos el formulario desde la app registration
from registration.forms import TypeUserForm, UserCreationFormWithEmail

# En las vistas cargamos todos los datos que necesitaremos mostrar
# en las template, en este caso las CCBV hacen todo automaticamente,
# son maravillosas.

# Los template de CCBV deben llevar el nombre del modelo y la funcion
# typeuser_list, typeuser_detail, typeuser_update_form
# el unico que cambia es el delete, ya qu el template es de confirmacion
# typeuser_confirm_delete

@method_decorator(login_required, name='dispatch')
class TypeUserList(ListView):
    # Asignamos el modelo a la variable model, como nos dice
    # la doc de CCBV de django ( http://ccbv.co.uk/ )
    model = TypeUser
    # Tambien es posible paginar con
    # paginated_by = 8
    # Esto quiere decir que mostrara 8 registros por pagina

@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class TypeUserUpdate(UpdateView):
    # Asignamos el objeto en la variable
    model = TypeUser
    # Utilizamos el mismo formulario creado en registratios
    form_class = TypeUserForm
    # Asignamos el nombre que tendra el formulario, aparte de typeuser
    template_name_suffix = '_update_form'
    # Asignamos a donde iremos cuando terminemos
    success_url = reverse_lazy('typeUser')

@method_decorator(login_required, name='dispatch')
class TypeUserDelete(DeleteView):
    # Asignamos el objeto en la variable
    model = TypeUser
    # Asignamos a donde iremos cuando terminemos
    success_url = reverse_lazy('typeUser')



@method_decorator(login_required, name='dispatch')
class UserList(ListView):
    model = User
    template_name = 'registration/user_list.html'
    paginate_by = 10

@method_decorator(login_required, name='dispatch')
class UserCreate(CreateView):
    # Asignamos el modelo a la variable
    model = User
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

@method_decorator(login_required, name='dispatch')
class UserUpdate(UpdateView):
    # Asignamos el objeto en la variable
    model = TypeUser
    # Utilizamos el mismo formulario creado en registratios
    form_class = TypeUserForm
    # Asignamos el nombre que tendra el formulario, aparte de typeuser
    template_name_suffix = '_update_form'
    # Asignamos a donde iremos cuando terminemos
    success_url = reverse_lazy('typeUser')

@method_decorator(login_required, name='dispatch')
class UserDelete(DeleteView):
    # Asignamos el objeto en la variable
    model = TypeUser
    # Asignamos a donde iremos cuando terminemos
    success_url = reverse_lazy('typeUser')



class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'core/user.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'

    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control mb-2','placeholder':'Nombre de usuario'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Direccion de email'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2','placeholder':'Contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2','placeholder':'Repite la contraseña'})
        return form


def home(request):
    return render(request, 'registration/login.html')


@login_required
def profile(request):
    return render(request, 'core/index.html')

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