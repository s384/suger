from django.db import models
from registration.models import Area
from cargos.models import Cargo
from django.template.defaultfilters import slugify

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
	duracion_horas = models.DecimalField(default = 7.5, max_digits = 4, decimal_places = 1)
	tipo_continuidad = models.BooleanField(choices=end_type)
	fecha_fin = models.DateField(null = True, blank = True)
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")
	slug = models.SlugField(max_length=100, verbose_name="Slug")

	class Meta:
		ordering = ['nombre','area']
		verbose_name = "Turno"
		verbose_name_plural = "Turnos"

	def __str__(self):
		return self.nombre

	def save(self, *args, **kwargs):
		self.slug = slugify(self.nombre)
		super(Turnos, self).save(*args, **kwargs)

class DetalleTurnos(models.Model):
	turno = models.ForeignKey(Turnos, on_delete=models.CASCADE, related_name="turno_detalle")
	cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name="cargo_detalle")
	cantidad = models.PositiveSmallIntegerField(default = 0)
