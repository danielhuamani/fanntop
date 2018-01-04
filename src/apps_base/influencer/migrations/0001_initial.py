# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-28 03:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Influencer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_trash', models.BooleanField(default=False, verbose_name='is trash')),
                ('position', models.IntegerField(default=1, verbose_name='Position')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('image', models.ImageField(upload_to='influencer/%Y/%m/%d', verbose_name='Influencer')),
            ],
            options={
                'verbose_name': 'Influencer',
                'verbose_name_plural': 'Influencers',
            },
        ),
        migrations.CreateModel(
            name='InfluencerSeo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=120)),
                ('title', models.CharField(max_length=120, verbose_name='title')),
                ('meta_description', models.CharField(blank=True, max_length=255, verbose_name='description')),
                ('influencer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='influencer_influencerseo', to='influencer.Influencer')),
            ],
            options={
                'verbose_name': 'InfluencerSeo',
                'verbose_name_plural': 'InfluencerSeos',
            },
        ),
    ]