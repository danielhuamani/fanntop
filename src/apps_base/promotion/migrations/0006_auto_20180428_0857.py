# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-28 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0005_coupon_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='prefix',
            field=models.CharField(max_length=120, unique=True, verbose_name='Code Coupon'),
        ),
    ]
