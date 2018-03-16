# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-14 02:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_customer_is_send_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Nacimiento'),
        ),
        migrations.AlterField(
            model_name='customershippingaddress',
            name='reference',
            field=models.CharField(blank=True, max_length=255, verbose_name='Referencia'),
        ),
    ]
