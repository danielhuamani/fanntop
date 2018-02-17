from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from django.db import transaction
from apps_base.attribute.serializers import AttributeOptionSerializer, AttributeSerializer
from sorl.thumbnail import get_thumbnail
from .models import ProductClass, Product, ProductAttributeValue, ProductGaleryImage, ProductImage
from .utils import generate_sku


class ProductSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(required=False, max_length=100, allow_blank=True)
    attribute_option = AttributeOptionSerializer(many=True)

    class Meta:
        model = Product
        fields = ['is_featured', 'id', 'attribute_option', 'sku', 'stock', 'price', 'is_active']


    def validate(self, data):
        #other wise you can set default value of age here,
        if not data.get('sku', None): #this conditon will be true only when age = serializer.IntergerField(required=False)
            data['sku'] = generate_sku()
        return data


class ProductGaleryImageSerializer(serializers.ModelSerializer):
    # product = serializers.IntegerField()
    product = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProductGaleryImage
        fields = ['image', 'product_class', 'product']

    @transaction.atomic
    def create(self, validated_data):
        product = validated_data.pop('product', None)
        product_galery_image = super(ProductGaleryImageSerializer, self).create(validated_data)
        is_featured = False
        if ProductImage.objects.filter(product_id=product).exists():
            is_featured = True
        ProductImage.objects.create(
            product_image=product_galery_image, product_id=product, is_featured=is_featured)
        return product_galery_image


class ProductImageSerializer(serializers.ModelSerializer):
    image_crop = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['is_featured', 'product_image', 'product', 'image_crop']


    def get_image_crop(self, obj):
        crop = get_thumbnail(obj.product_image.image, '180x180', crop='center', quality=99)
        return self.context['request'].build_absolute_uri(crop.url)


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=ProductAttributeValue()._meta.get_field('id'), required=False)

    class Meta:
        model = ProductAttributeValue
        fields = [
            'attribute', 'value_text','value_boolean',
            'value_input','value_multi_option','value_option', 'id'
        ]


class ProductClassSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    product_class_products = ProductSerializer(many=True)
    product_class_product_attr_value = ProductAttributeValueSerializer(many=True)
    family_name = serializers.SerializerMethodField()

    class Meta:
        model = ProductClass
        fields = ['id', 'influencer', 'category', 'name',  'description', 'is_variation',
             'title', 'slug', 'meta_description', 'product_class_product_attr_value',
             'product_class_products', 'family', 'attribute', 'characteristics', 'family_name']


    def get_family_name(self, obj):
        return obj.family.name

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
                print(product.get('attribute_option'), '----', product)
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

    @transaction.atomic
    def update(self, instance, validated_data):
        product_class_product_attr_value = []
        if validated_data.get('product_class_product_attr_value'):
            product_class_product_attr_value = validated_data.pop('product_class_product_attr_value')
        instance = super(ProductClassSerializer, self).update(instance, validated_data)
        for attr_value in product_class_product_attr_value:
            id = ''
            if attr_value.get('id', None) or attr_value.get('id', None) == 0:
                id = attr_value.pop('id')
            if id:
                ProductAttributeValue.objects.filter(id=int(id)).update(**attr_value)
            else:
                ProductAttributeValue.objects.create(product_class=instance, **attr_value)
        return instance


class ProductClassAttributeSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    attribute = AttributeSerializer(many=True)

    class Meta:
        model = ProductClass
        fields = ['is_variation', 'attribute']