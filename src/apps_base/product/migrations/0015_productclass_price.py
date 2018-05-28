# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-26 22:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_auto_20180308_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='productclass',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='price'),
        ),
    ]