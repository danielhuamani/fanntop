# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-03 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0013_auto_20180403_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerproductfavorite',
            name='code',
            field=models.CharField(max_length=255),
        ),
    ]
