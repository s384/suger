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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type_user = models.ForeignKey(TypeUser, related_name="relacion_typeuser",
            on_delete=models.CASCADE, verbose_name="Tipo de usuario")
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True,
            verbose_name="Direccion")
    telefono = models.CharField(max_length=13, null=True, blank=True, 
            verbose_name="Numero de Telefono")
    email_confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ['user__firstname']

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        # print("Se acaba de crear un usuario y su perfil enlazado")