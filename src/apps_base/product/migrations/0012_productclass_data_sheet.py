# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-22 12:14
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_auto_20180221_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='productclass',
            name='data_sheet',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=''),
            preserve_default=False,
        ),
    ]
