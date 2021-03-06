from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from registration.models import Area

# Create your models here.

class Cargo(models.Model):
    area = models.ForeignKey(Area, on_delete = models.SET_NULL, verbose_name = "dependiente de",
                             related_name="Area_cargo", null=True)
    titulo = models.CharField(max_length=100, verbose_name="título del cargo")
    slug = models.SlugField(max_length=100, verbose_name="Slug")
    descripcion = models.TextField(null = True, blank = True)

    class Meta:
        ordering = ['area', 'titulo']

    def __str__(self):
        if self.area:
            nombre = self.titulo + " - " + self.area.nombre
        else:
            nombre = self.titulo
        return nombre

    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo)
        super(Cargo, self).save(*args, **kwargs)
