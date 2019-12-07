from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tareas(models.Model):
    priority = [(1, "Baja"),(2, "Media"),(3,"Alta")]

    titulo = models.CharField(max_length=100)
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="super_tarea")
    prioridad = models.PositiveSmallIntegerField(choices=priority)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, related_name="respo_tarea")
    descripcion = models.TextField()
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_termino = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")

    class Meta:
        ordering = ['created']
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"

    def __str__(self):
        return self.titulo