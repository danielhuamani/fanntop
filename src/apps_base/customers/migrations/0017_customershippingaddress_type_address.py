# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-09-27 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0016_auto_20180417_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='customershippingaddress',
            name='type_address',
            field=models.CharField(choices=[('CASA', 'Casa'), ('OFICINA', 'Oficina'), ('DEPARTAMENTO', 'Departamento'), ('CASA_PLAYA', 'Casa de playa'), ('CASA_CAMPO', 'Casa de campo'), ('OTRO', 'Otro')], default=1, max_length=120, verbose_name='Type address'),
            preserve_default=False,
        ),
    ]
