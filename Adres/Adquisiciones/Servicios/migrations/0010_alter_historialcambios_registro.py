# Generated by Django 5.0.1 on 2024-02-03 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Servicios', '0009_historialcambios'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialcambios',
            name='registro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historialcambios_set', to='Servicios.registro'),
        ),
    ]