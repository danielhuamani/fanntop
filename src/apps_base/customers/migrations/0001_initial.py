# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-16 05:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.CharField(max_length=120, verbose_name='Document')),
                ('type_document', models.CharField(choices=[('DNI', 'DNI'), ('CE', 'Carnet de extranjería')], max_length=120, verbose_name='Type Document')),
                ('is_offers_news', models.BooleanField(default=False, verbose_name='offers and news')),
                ('terms_conditions', models.BooleanField(default=True, verbose_name='Terms and Conditions')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=120, verbose_name='Gender')),
                ('phone', models.CharField(blank=True, max_length=120, verbose_name='Phone')),
                ('birth_date', models.DateField(verbose_name='Fecha Nacimiento')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_customer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Customers',
                'verbose_name': 'Customer',
            },
        ),
    ]
