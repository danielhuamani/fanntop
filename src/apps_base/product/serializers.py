from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from django.db import transaction
from apps_base.attribute.serializers import AttributeOptionSerializer
from .models import ProductClass, Product, ProductAttributeValue, ProductGaleryImage
from .utils import generate_sku


class ProductSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(required=False, max_length=100, allow_blank=True)
    attribute_option = AttributeOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['is_featured', 'id', 'attribute_option', 'sku', 'stock', 'price', 'is_active']


    def validate(self, data):
        #other wise you can set default value of age here,
        if not data.get('sku', None): #this conditon will be true only when age = serializer.IntergerField(required=False)
            data['sku'] = generate_sku()
        return data


class ProductGaleryImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductGaleryImage
        fields = ['image', 'product_class']


class ProductAttributeValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttributeValue
        fields = [
            'attribute', 'value_text','value_boolean',
            'value_input','value_multi_option','value_option'
        ]


class ProductClassSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    product_class_products = ProductSerializer(many=True)
    product_class_product_attr_value = ProductAttributeValueSerializer(many=True)

    class Meta:
        model = ProductClass
        fields = ['id', 'influencer', 'category', 'name',  'description', 'is_variation',
             'title', 'slug', 'meta_description', 'product_class_product_attr_value',
             'product_class_products', 'family', 'attribute']


    @transaction.atomic
    def create(self, validated_data):
        product_class_product_attr_value = validated_data.pop('product_class_product_attr_value')
        product_class_products = validated_data.pop('product_class_products')
        product_class = super(ProductClassSerializer, self).create(validated_data)
        if product_class.is_variation and product_class_products:
            for product in product_class_products:
                product_create = Product.objects.create(
                    product_class=product_class,
                    sku=product.get('sku'),
                    stock=product.get('stock'),
                    price=product.get('price'),
                    is_featured=product.get('is_featured'),
                    is_variation=True
                )
                product_create.attribute_option.add(*product.get('attribute_option'))
        else:
             Product.objects.create(
                product_class=product_class,
                sku='',
                stock=0,
                price=0,
                is_featured=True,
                is_variation=False
            )
        for product_class_attr_value in product_class_product_attr_value:
            ProductAttributeValue.objects.create(product_class=product_class, **product_class_attr_value)
        return product_class