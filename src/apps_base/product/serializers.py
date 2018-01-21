from rest_framework import serializers
from .models import ProductClass


class ProductClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductClass
        fields = ['influencer', 'category', 'name',  'description', 'is_variation',
             'title', 'slug', 'meta_description']




