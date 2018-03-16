# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-16 21:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20180313_2127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_trash', models.BooleanField(default=False, verbose_name='is trash')),
                ('position', models.IntegerField(default=1, verbose_name='Position')),
                ('slug', models.CharField(max_length=120)),
                ('meta_description', models.CharField(blank=True, max_length=255, verbose_name='description')),
                ('title', models.CharField(max_length=120, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Pages',
                'verbose_name_plural': 'Pagess',
            },
        ),
    ]
