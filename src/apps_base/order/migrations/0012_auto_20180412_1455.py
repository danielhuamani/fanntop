# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-12 19:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0004_auto_20180412_1452'),
        ('order', '0011_auto_20180407_1233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='coupon',
        ),
        migrations.AddField(
            model_name='order',
            name='coupon_discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coupon_orders', to='promotion.Coupon'),
        ),
    ]
