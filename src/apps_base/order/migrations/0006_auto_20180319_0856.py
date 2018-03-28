# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-19 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_order_type_status_shipping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='type_status',
            field=models.CharField(blank=True, choices=[('PG', 'Pagado'), ('DN', 'Denegado'), ('RC', 'Rechazado'), ('PE', 'Pendiente'), ('PR_1', 'Pendiente'), ('PR_2', 'Proceso Paso 2'), ('CN', 'Cancelado')], max_length=255, verbose_name='type_status'),
        ),
    ]