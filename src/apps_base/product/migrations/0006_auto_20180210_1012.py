# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-10 15:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20180210_0941'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productattributevalue',
            old_name='product',
            new_name='product_class',
        ),
    ]