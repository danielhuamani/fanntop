# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-07 19:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20180307_1339'),
        ('customers', '0003_customershippingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='customershippingaddress',
            name='order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_shipping_adress_customers', to='order.OrderShippingAddress'),
        ),
    ]
