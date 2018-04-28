from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from sorl.thumbnail import get_thumbnail
from apps_base.product.models import Product, ProductClass, ProductAttributeValue
from apps_base.attribute.models import AttributeOption


class AttributeOptionSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    name_attr = serializers.SerializerMethodField()

    class Meta:
        model = AttributeOption
        fields = [
            'id', 'attr', 'option', 'name_attr'
        ]

    def get_name_attr(self, obj):
        return obj.attribute.name


class ProductAttributeValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttributeValue
        fields = [
            'attribute', 'value_text','value_boolean',
            'value_input','value_multi_option','value_option'
        ]


class ProductSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(required=False, max_length=100, allow_blank=True)
    # product_attribute_option = serializers.SerializerMethodField()
    image_crop = serializers.SerializerMethodField()
    attribute_option = AttributeOptionSerializer(many=True)

    class Meta:
        model = Product
        fields = ['is_featured', 'id', 'attribute_option', 'sku', 'stock',
             'price', 'is_active', 'image_crop']

    def get_image_crop(self, obj):
        crop = get_thumbnail(obj.get_image(), '50x50', crop='center', quality=99)
        return self.context['request'].build_absolute_uri(crop.url)


    # def get_product_attribute_option(self, obj):
    #     return AttributeOptionSerializer(obj.attribute_option, many=True).data


class ProductClassSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    product_class_products = ProductSerializer(many=True)
    product_class_product_attr_value = ProductAttributeValueSerializer(many=True)
    family_name = serializers.SerializerMethodField()

    class Meta:
        model = ProductClass
        fields = ['id', 'name',  'description', 'is_variation',
             'title', 'slug', 'meta_description', 'product_class_product_attr_value',
             'product_class_products', 'attribute', 'characteristics', 'family_name',
             'is_published', 'data_sheet']

    def get_family_name(self, obj):
        return obj.family.name