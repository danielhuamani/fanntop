# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-18 00:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_auto_20180412_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount_stock',
            field=models.BooleanField(default=False),
        ),
    ]
