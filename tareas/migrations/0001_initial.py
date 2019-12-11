# Generated by Django 2.2.7 on 2019-12-11 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tareas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('prioridad', models.PositiveSmallIntegerField(choices=[(1, 'Baja'), (2, 'Media'), (3, 'Alta')])),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField(auto_now_add=True)),
                ('fecha_termino', models.DateField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualizacion')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respo_tarea', to=settings.AUTH_USER_MODEL)),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='super_tarea', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created'],
                'verbose_name_plural': 'Tareas',
                'verbose_name': 'Tarea',
            },
        ),
        migrations.CreateModel(
            name='SolicitudTarea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, verbose_name='Slug')),
                ('descripcion', models.TextField()),
                ('img_referencia', models.ImageField(blank=True, null=True, upload_to='solicitud')),
                ('prioridad', models.PositiveSmallIntegerField(choices=[(1, 'Baja'), (2, 'Media'), (3, 'Alta')])),
                ('estado_solicitud', models.PositiveSmallIntegerField(choices=[(1, 'No Revisado'), (2, 'En revisión'), (3, 'Rechazada'), (4, 'Aprovada')])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualizacion')),
                ('area_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='area_solicitud', to='registration.Area')),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_solicitud', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created'],
                'verbose_name_plural': 'Solicitudes de tareas',
                'verbose_name': 'Solicitud de tarea',
            },
        ),
    ]
