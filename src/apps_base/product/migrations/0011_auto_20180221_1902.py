# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-22 00:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attribute', '0006_attribute_slug'),
        ('product', '0010_auto_20180212_2024'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productattributevalue',
            unique_together=set([('attribute', 'product_class')]),
        ),
    ]
