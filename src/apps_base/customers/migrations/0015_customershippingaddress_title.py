# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-17 02:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0014_auto_20180403_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='customershippingaddress',
            name='title',
            field=models.CharField(blank=True, max_length=120, verbose_name='title'),
        ),
    ]
