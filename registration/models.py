from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

# Funcion para borrar la imagen de perfil cuando se actualiza
def custom_upload_to(instance, filename):
    # Obtenemos el objeto, consultamos la db por el pk de la instancia
    old_instance = Profile.objects.get(pk=instance.pk)
    # Borramos el avatar de la instancia
    old_instance.avatar.delete()
    # Retornamos el nombre
    return 'profiles/' + filename

# Modelo para el tipo de usuario
class TypeUser(models.Model):
    # Nombre del tipo de usuario
    nombre = models.CharField(max_length=50, verbose_name='Nombre tipo de usuario')
    # Campo slug para mostrar url, cuando necesitemos acceder al objeto
    slug = models.SlugField(max_length=100, verbose_name="Slug")
    # Fecha de creacion del objeto
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    # Fecha de actualizacion del mismo
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")

    # Clase meta, ordenamos los modelos por el nombre, esto se ve cuando
    # llamamos los objetos, se retornan ordenados por este valor
    class Meta:
        ordering = ['nombre']

    # funcion str, retorna el nombre cuando llamamos al objeto, sino diria objeto + pk
    def __str__(self):
        return self.nombre

    # Funcion save, esta la creamos para editar el campo slug de manera automatica
    # reemplazando los espacios por guiones, para ser utilizado en urls
    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(TypeUser, self).save(*args, **kwargs)


# Modelo para el tipo de usuario
class Area(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre de area')
    boss_user = models.OneToOneField(User, on_delete=models.CASCADE, 
                verbose_name="Encargado de area", null=True, blank=True)
    slug = models.SlugField(max_length=100, verbose_name="Slug")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Area, self).save(*args, **kwargs)

class SubArea(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre de sub-area')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name='area de dependencia')
    detalle_subarea = models.TextField(null = True, blank = True, verbose_name='Información adicional de SubArea')
    slug = models.SlugField(max_length=100, verbose_name="Slug")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")

    class Meta:
        ordering = ['area','nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(SubArea, self).save(*args, **kwargs)


class Profile(models.Model):
    user_options = [(1, "Administrador"),(2, "Supervisor"),(3, "Trabajador")]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #type_user = models.ForeignKey(TypeUser, related_name="relacion_typeuser",
            #on_delete=models.CASCADE, verbose_name="Tipo de usuario",
            #null=True, blank=True)
    type_user = models.PositiveSmallIntegerField(choices=user_options, default=3)
    area_user = models.ForeignKey(SubArea, on_delete="CASCADE", verbose_name="SubArea",
            null=True, blank=True)
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True,
            verbose_name="Direccion")
    telefono = models.CharField(max_length=13, null=True, blank=True, 
            verbose_name="Numero de Telefono")
    email_confirmed = models.BooleanField(default=False)
    first_login = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")

    class Meta:
        ordering = ['user__first_name']

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        # print("Se acaba de crear un usuario y su perfil enlazado")