from django.db import models
from django.contrib.auth.models import User
from registration.models import Area
from django.template.defaultfilters import slugify

# Create your models here.

class SolicitudTarea(models.Model):
    priority = [(1,"Baja"),(2,"Media"),(3,"Alta")]
    opciones_estado = [(1, "No Revisado"), (2, "En revisión"), (3, "Rechazada"), (4, "Aprovada")]

    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, verbose_name="Slug")
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario_solicitud")
    area_destino = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="area_solicitud")
    descripcion = models.TextField()
    img_referencia = models.ImageField(upload_to="solicitud", null=True, blank=True)
    prioridad = models.PositiveSmallIntegerField(choices=priority)
    estado_solicitud = models.PositiveSmallIntegerField(choices=opciones_estado)

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")

    class Meta:
        ordering = ['created']
        verbose_name = "Solicitud de tarea"
        verbose_name_plural = "Solicitudes de tareas"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo)
        super(SolicitudTarea, self).save(*args, **kwargs)


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
