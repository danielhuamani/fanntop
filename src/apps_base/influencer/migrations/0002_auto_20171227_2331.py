# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-28 04:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('influencer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='influencer',
            name='meta_description',
            field=models.CharField(blank=True, max_length=255, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='influencer',
            name='title',
            field=models.CharField(default='', max_length=120, verbose_name='title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='influencer',
            name='url',
            field=models.CharField(default='', max_length=120),
            preserve_default=False,
        ),
    ]
