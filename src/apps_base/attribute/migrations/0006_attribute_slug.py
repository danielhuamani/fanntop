# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-22 00:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attribute', '0005_auto_20180215_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='slug',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]