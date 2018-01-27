# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-27 14:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attribute', '0004_auto_20180118_0651'),
        ('product', '0002_productclass_family'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_text', models.TextField(blank=True, null=True, verbose_name='Text')),
                ('value_boolean', models.NullBooleanField(verbose_name='Boolean')),
                ('value_input', models.CharField(blank=True, max_length=255, verbose_name='Input')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attribute_product_attr_value', to='attribute.Attribute', verbose_name='Attribute')),
            ],
        ),
        migrations.AddField(
            model_name='productclass',
            name='attribute',
            field=models.ManyToManyField(related_name='attribute_product_class', to='attribute.Attribute'),
        ),
        migrations.AddField(
            model_name='productattributevalue',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_class_product_attr_value', to='product.ProductClass', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='productattributevalue',
            name='value_multi_option',
            field=models.ManyToManyField(blank=True, related_name='attr_option_product_attr_multi_value', to='attribute.AttributeOption', verbose_name='Value multi option'),
        ),
        migrations.AddField(
            model_name='productattributevalue',
            name='value_option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attr_option_product_attr_value', to='attribute.AttributeOption', verbose_name='Value option'),
        ),
    ]
