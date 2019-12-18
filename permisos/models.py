from django.db import models
from turnos.models import Turnos, DetalleTurnos
from cargos.models import Cargo
from django.contrib.auth.models import User

from django.template.defaultfilters import slugify

# Create your models here.

class SolicitudPermisos(models.Model):
	tipos_permisos = [(0, "Ausencia"),(1, "Permiso Administrativo"),(2,"Vacaciones"),(3,"Licencia Médica"),(4,"Atraso"),(5,"Salida Anticipada")]
	tipos_jornadas = [(0, "Completa"),(1, "Parcial Mañana"),(2, "Parcial Tarde")]
	opciones_estado = [(1, "No Revisado"), (2, "En revisión"), (3, "Rechazada"), (4, "Aprovada")]

	titulo = models.CharField(max_length = 100,verbose_name = "título de la solicitud de permiso")
	usuario = models.ForeignKey(User, on_delete=models.CASCADE,related_name="usuarios_solicitudes_permisos")
	comentario = models.TextField()
	tipo_permiso = models.PositiveSmallIntegerField(choices = tipos_permisos)
	tipo_jornada = models.PositiveSmallIntegerField(choices = tipos_jornadas, null = True ,blank = True)
	fecha_inicio = models.DateField()
	dias_permiso = models.PositiveSmallIntegerField(default = 1)
	horas_permiso = models.PositiveSmallIntegerField(null = True ,blank = True)
	img_referencia = models.ImageField(upload_to = "Permisos", null = True ,blank = True)
	estado_solicitud = models.PositiveSmallIntegerField(choices=opciones_estado, default = 1)

	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")

	class Meta:
		ordering = ['created']
		verbose_name = "Solicitud de permiso"
		verbose_name_plural = "Solicitudes de permisos"

	def __str__(self):
		nombre = self.usuario.get_full_name()
		return nombre