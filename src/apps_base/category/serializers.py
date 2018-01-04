from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from .models import Category


class CategorySerializer(QueryFieldsMixin, serializers.ModelSerializer):
    category_categories = serializers.SerializerMethodField(
        read_only=True, method_name="get_child_categories")

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'image', 'position',
            'is_active', 'title', 'slug', 'meta_description', 'category', 'category_categories'
        ]

    def get_child_categories(self, obj):
        serializer = CategorySerializer(
            instance=obj.category_categories.all(),
            many=True
        )
        return serializer.data