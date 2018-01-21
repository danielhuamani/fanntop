# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-18 11:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attribute', '0004_auto_20180118_0651'),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Family',
                'verbose_name_plural': 'Familys',
            },
        ),
        migrations.CreateModel(
            name='FamilyGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('family', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='family_familygroup', to='family.Family')),
            ],
            options={
                'verbose_name': 'FamilyGroup',
                'verbose_name_plural': 'FamilyGroups',
            },
        ),
        migrations.CreateModel(
            name='FamilyGroupAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_trash', models.BooleanField(default=False, verbose_name='is trash')),
                ('is_required', models.BooleanField(default=False, verbose_name='Obligatorio')),
                ('atribute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attribute_familygroupatribute', to='attribute.Attribute')),
                ('family_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='familygroup_familygroupatribute', to='family.FamilyGroup')),
            ],
            options={
                'verbose_name': 'Family Group Atribute',
                'verbose_name_plural': 'Family Group Atribute',
            },
        ),
    ]
