from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from .models import Category


class CategorySerializer(QueryFieldsMixin, serializers.ModelSerializer):
    # category_categories = serializers.SerializerMethodField(
    #     read_only=True, method_name="get_child_categories")
    levels_category =  serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'image', 'position', 'levels_category',
            'is_active', 'title', 'slug', 'meta_description', 'category', 'category_categories'
        ]

    # def get_child_categories(self, obj):
    #     serializer = CategorySerializer(
    #         instance=obj.category_categories.all(),
    #         many=True
    #     )
    #     return serializer.data

    def get_levels_category(self, obj):
        category = obj
        list_category = []
        if category.category:
            list_category.append(category.category.id)
            if category.category.category:
                list_category.append(category.category.category.id)

        return list(reversed(list_category))