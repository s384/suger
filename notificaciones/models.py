from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notificacion(models.Model):
    estado_noti = [(0, 'Pendiente'),(1, 'Revisada')]
    priority = [(1,"Baja"),(2,"Media"),(3,"Alta")]

    asunto = models.CharField(max_length=100, verbose_name="Asunto")
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion")
    usuario = models.ForeignKey(User, on_delete="CASCADE")
    prioridad = models.PositiveSmallIntegerField(choices=priority)
    estado = models.BooleanField(choices=estado_noti, default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.asunto