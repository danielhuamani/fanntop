from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'image', 'position',
            'is_active', 'title', 'slug', 'meta_description', 'category'
        ]

