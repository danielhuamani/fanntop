# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-03 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='birth_date',
            field=models.DateField(null=True, verbose_name='Fecha Nacimiento'),
        ),
    ]
