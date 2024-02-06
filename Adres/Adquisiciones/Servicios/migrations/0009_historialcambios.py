# Generated by Django 5.0.1 on 2024-02-01 19:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Servicios', '0008_remove_registro_id_registro_idregistro'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialCambios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campo_modificado', models.CharField(max_length=255)),
                ('valor_anterior', models.CharField(max_length=255)),
                ('nuevo_valor', models.CharField(max_length=255)),
                ('fecha_modificacion', models.DateTimeField(auto_now_add=True)),
                ('registro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Servicios.registro')),
            ],
        ),
    ]