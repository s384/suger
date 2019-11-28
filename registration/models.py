from django.db import models

# Create your models here.

class TypeUser(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre tipo de usuario')
    slug = models.SlugField(max_length=100, verbose_name="Slug")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

