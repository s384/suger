# Generated by Django 2.2.7 on 2019-12-08 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turnos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('tipo_turno', models.BooleanField(choices=[(0, 'Fijo'), (1, 'Rotativo')])),
                ('fecha_inicio', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('duracion_horas', models.DurationField()),
                ('duracion_rotacion', models.DurationField(blank=True, null=True)),
                ('tipo_continuidad', models.BooleanField(choices=[(0, 'Temporal'), (1, 'Permanente')])),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualizacion')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='area_turnos', to='registration.Area')),
            ],
            options={
                'verbose_name_plural': 'Turnos',
                'verbose_name': 'Turno',
                'ordering': ['nombre', 'area'],
            },
        ),
    ]