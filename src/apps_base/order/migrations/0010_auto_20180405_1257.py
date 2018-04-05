# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-05 17:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0003_auto_20180404_1036'),
        ('order', '0009_auto_20180322_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coupon_order', to='promotion.CouponGenerate'),
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Envio'),
        ),
    ]