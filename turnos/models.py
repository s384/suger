from django.db import models
from registration.models import Area

# Create your models here.

class Turnos(models.Model):
	turn_type = [(0, "Fijo"),(1, "Rotativo")]
	end_type = [(0,"Temporal"),(1,"Permanente")]

	nombre = models.CharField(max_length=100)
	descripcion = models.TextField(null = True, blank = True)
	area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="area_turnos")
	tipo_turno = models.BooleanField(choices=turn_type)  
	fecha_inicio = models.DateField()
	hora_inicio = models.TimeField()
	duracion_horas = models.PositiveSmallIntegerField(default = 0)
	tipo_continuidad = models.BooleanField(choices=end_type)
	fecha_fin = models.DateField(null = True, blank = True)
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")

	class Meta:
		ordering = ['nombre','area']
		verbose_name = "Turno"
		verbose_name_plural = "Turnos"

	def __str__(self):
		return self.nombre

