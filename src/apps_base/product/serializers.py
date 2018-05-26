from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from django.db import transaction
from apps_base.attribute.serializers import AttributeOptionSerializer, AttributeSerializer
from sorl.thumbnail import get_thumbnail
from .models import ProductClass, Product, ProductAttributeValue, ProductGaleryImage, ProductImage
from .utils import generate_sku


class ProductSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(required=False, max_length=100, allow_blank=True)
    product_attribute_option = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['is_featured', 'id', 'attribute_option', 'sku', 'stock',
             'price', 'is_active', 'product_attribute_option']


    def validate(self, data):
        #other wise you can set default value of age here,
        if not data.get('sku', None): #this conditon will be true only when age = serializer.IntergerField(required=False)
            data['sku'] = generate_sku()
        return data

    def get_product_attribute_option(self, obj):
        return AttributeOptionSerializer(obj.attribute_option, many=True).data


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
    influencer_name = serializers.SerializerMethodField()

    class Meta:
        model = ProductClass
        fields = ['id', 'influencer', 'category', 'name',  'description', 'is_variation',
             'title', 'slug', 'meta_description', 'product_class_product_attr_value',
             'product_class_products', 'family', 'attribute', 'characteristics', 'family_name',
             'is_published', 'price', 'influencer_name']

    def get_influencer_name(self, obj):
        return obj.influencer.name

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
                    is_variation=True,
                    is_active=False
                )
                product_create.attribute_option.add(*product.get('attribute_option'))
        else:
             Product.objects.create(
                product_class=product_class,
                sku='',
                stock=0,
                price=0,
                is_featured=True,
                is_variation=False,
                is_active=False
            )
        update_json_data_sheet = False
        for product_class_attr_value in product_class_product_attr_value:
            update_json_data_sheet = True
            if product_class_attr_value.get('id') or product_class_attr_value.get('id') == 0:
                product_class_attr_value.pop('id')
            ProductAttributeValue.objects.create(product_class=product_class, **product_class_attr_value)
        # add data extra
        if update_json_data_sheet:
            product_class.attribute.all()
            data = {
                'ficha': []
            }
            for attr in product_class.family.family_familygroupatribute.filter(
                attribute__is_variation=False).prefetch_related('attribute'):
                data['ficha'].append({
                    'name': attr.attribute.name_store,
                    'value': product_class.product_class_product_attr_value.all().get(
                        attribute_id=attr.attribute_id).get_value()
                })
            product_class.data_sheet = data
            product_class.save()
        return product_class

    @transaction.atomic
    def update(self, instance, validated_data):
        product_class_product_attr_value = []
        # if validated_data.get('product_class_product_attr_value'):
        product_class_product_attr_value = validated_data.pop('product_class_product_attr_value')
        print(validated_data, '-validated_data')
        instance = super(ProductClassSerializer, self).update(instance, validated_data)
        update_json_data_sheet = False
        for attr_value in product_class_product_attr_value:
            update_json_data_sheet = True
            id = ''
            if attr_value.get('id', None) or attr_value.get('id', None) == 0:
                id = attr_value.pop('id')
            if id:
                ProductAttributeValue.objects.filter(id=int(id)).update(**attr_value)
            else:
                ProductAttributeValue.objects.create(product_class=instance, **attr_value)
        if update_json_data_sheet:
            data = {
                'ficha': []
            }
            for attr in instance.family.family_familygroupatribute.filter(
                attribute__is_variation=False).prefetch_related('attribute'):
                data['ficha'].append({
                    'name': attr.attribute.name_store,
                    'value': instance.product_class_product_attr_value.all().get(
                        attribute_id=attr.attribute_id).get_value()
                })
            instance.data_sheet = data
            instance.save()
        return instance


class ProductClassAttributeSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    attribute = AttributeSerializer(many=True)

    class Meta:
        model = ProductClass
        fields = ['is_variation', 'attribute']