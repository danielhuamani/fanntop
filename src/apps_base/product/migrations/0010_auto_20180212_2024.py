# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-13 01:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_product_is_variation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productclass',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products Class'},
        ),
        migrations.AddField(
            model_name='productclass',
            name='characteristics',
            field=models.TextField(default='', verbose_name='characteristics'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productclass',
            name='attribute',
            field=models.ManyToManyField(blank=True, related_name='attribute_product_class', to='attribute.Attribute'),
        ),
        migrations.AlterField(
            model_name='productgaleryimage',
            name='name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Name'),
        ),
    ]