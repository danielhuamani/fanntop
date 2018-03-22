# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-22 14:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ubigeo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComplaintsBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=120, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=120, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=120, verbose_name='Email')),
                ('document', models.CharField(max_length=120, verbose_name='Document')),
                ('type_document', models.CharField(choices=[('DNI', 'DNI'), ('CE', 'Carnet de extranjería')], max_length=120, verbose_name='Type Document')),
                ('phone', models.CharField(max_length=120, verbose_name='Celephone')),
                ('address', models.CharField(max_length=250, verbose_name='Address')),
                ('type_claim', models.CharField(choices=[('C', 'Reclamo'), ('Q', 'Queja')], max_length=5, verbose_name='Type Claim')),
                ('detail', models.TextField()),
                ('pedido', models.CharField(max_length=120)),
                ('well_contracted', models.CharField(choices=[('SS', 'Servicio'), ('PR', 'Producto')], max_length=120)),
                ('desciption', models.TextField()),
                ('mount', models.PositiveIntegerField()),
                ('ubigeo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ubigeo_complaints_book', to='ubigeo.Ubigeo')),
            ],
            options={
                'verbose_name_plural': 'ComplaintsBook',
                'verbose_name': 'ComplaintsBook',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=120, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=120, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=120, verbose_name='Email')),
                ('phone', models.CharField(max_length=120, verbose_name='Celephone')),
                ('subject', models.CharField(max_length=120, verbose_name='Subject')),
                ('message', models.TextField(verbose_name='Message')),
            ],
            options={
                'verbose_name_plural': 'Contacts',
                'verbose_name': 'Contact',
            },
        ),
        migrations.CreateModel(
            name='Suscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_trash', models.BooleanField(default=False, verbose_name='is trash')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
            ],
            options={
                'verbose_name_plural': 'Suscriptions',
                'verbose_name': 'Suscription',
            },
        ),
    ]
