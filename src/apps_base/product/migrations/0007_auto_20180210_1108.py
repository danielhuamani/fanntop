# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-10 16:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('family', '0003_auto_20180120_1733'),
        ('product', '0006_auto_20180210_1012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productclass',
            name='family',
        ),
        migrations.AddField(
            model_name='productclass',
            name='family_fk',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='family_fk_product_class', to='family.Family'),
            preserve_default=False,
        ),
    ]