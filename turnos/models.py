from django.db import models
from registration.models import Area
from django.contrib.auth.models import User
from cargos.models import Cargo
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Turnos(models.Model):
	turn_type = [(0, "Fijo"),(1, "Rotativo")]
	end_type = [(0,"Temporal"),(1,"Permanente")]
	cantidad_horas = [(0, "Lunes a Viernes"),(1, "Lunes a Sábado"), (2, "Lunes a Viernes / Sábado")]

	nombre = models.CharField(max_length=100)
	descripcion = models.TextField(null = True, blank = True)
	area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="area_turnos")
	tipo_turno = models.BooleanField(choices=turn_type)
	fecha_inicio = models.DateField()
	hora_inicio = models.TimeField()
	duracion_horas = models.PositiveSmallIntegerField(choices=cantidad_horas)
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
	cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, 
		related_name="cargo_detalle", null=True, blank=True)
	cantidad = models.PositiveSmallIntegerField(default=0)


class TurnoUsuario(models.Model):
	turno = models.ForeignKey(Turnos, on_delete=models.CASCADE, related_name="turno_usuario")
	usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario_turno")

	def __str__(self):
		nombre = (self.turno.nombre + " - " + self.usuario.get_full_name() + 
			" - " + self.usuario.profile.cargo_user.titulo + 
			" - " + self.usuario.profile.cargo_user.area.nombre)
		return nombre

class HorarioUsuario(models.Model):
	inter = [(0,'Trabajado'), (1,'Intercambiado')]
	traba = [(0,'Trabajado'), (1,'Ausencia')]

	turno_usuario = models.ForeignKey(TurnoUsuario, on_delete=models.CASCADE,
					related_name="horario_turno")
	dia_semana = models.DateField(null=True, blank=True)
	hora_inicio = models.TimeField(null=True, blank=True)
	hora_fin = models.TimeField(null=True, blank=True)
	# Estado para intercambios de turnos
	intercambio = models.BooleanField(default=0, choices=inter)
	# Estado para cambio en solicitudes de permisos
	trabajado = models.BooleanField(default=0, choices=traba)

	def __str__(self):
		nombre = (self.turno_usuario.usuario.get_full_name() + " " +
			self.dia_semana.strftime("%a %d/%m") + " " +
			str(self.hora_inicio))
		return nombre