# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-31 17:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_productclass_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='productclass',
            name='process',
            field=models.CharField(choices=[('PASO1', 'Paso 1'), ('PASO2', 'Paso 2'), ('PASO3', 'Paso 3'), ('PASO4', 'Paso 4')], default='', max_length=120),
            preserve_default=False,
        ),
    ]
