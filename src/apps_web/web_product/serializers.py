from apps_base.product.models import ProductImage, Product, ProductClass
from apps_base.influencer.models import Influencer
from apps_base.attribute.models import Attribute, AttributeOption
from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from sorl.thumbnail import get_thumbnail


class AttributeOptionFilterSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = AttributeOption
        fields = [
            'id', 'attr', 'option', 'slug'
        ]


class AttributeFilterSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    attribute_options_query = serializers.SerializerMethodField()
    class Meta:
        model = Attribute
        fields = [
            'id', 'name', 'name_store', 'attribute_options_query', 'type_name', 'slug'
        ]

    def get_attribute_options_query(self, obj):
        query = AttributeOption.objects.filter(id__in=self.context.get('attribute_option_ids'), attribute_id=obj.id)
        return AttributeOptionFilterSerializer(query, many=True).data


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


    def get_image(self, obj):
        crop = get_thumbnail(obj.product_image.image, '264x250', crop='center', quality=99)
        return crop.url


class ProductSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['price', 'id', 'product_image']

    def get_product_image(self, obj):
        product_image = obj.product_product_images.order_by('-is_featured')
        # product_image_featured = product_image.filter(is_featured=True)
        # if product_image_featured.exists():
        #     product_image_featured = product_image_featured.prefetch_related('product_image').first()
        # else:
        #     product_image_featured = product_image.prefetch_related('product_image').first()
        return ProductImageSerializer(product_image.first()).data


class ProductClassSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    # product_variant = ProductSerializer(
    #     source='get_product_variant', read_only=True)
    product_variant = serializers.SerializerMethodField()

    class Meta:
        model = ProductClass
        fields = ['name', 'slug', 'id', 'product_variant']


    def get_product_variant(self, obj):
        print(self.context, 'context')
        attr_list = self.context.get('attr_list')
        if attr_list:
            product_variant = obj.product_class_products.filter(
                attribute_option__slug__in=attr_list).order_by('-is_featured')
        else:
            product_variant = obj.product_class_products.filter(is_active=True).order_by('-is_featured')
        # product_variant_featured = product_variant.filter(is_featured=True)
        # if product_variant_featured.exists():
        #     product_variant_featured = product_variant_featured.first()

        # else:
        product_variant_featured = product_variant.first()
        return ProductSerializer(product_variant_featured).data


class ProductImageDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image_big = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_big']


    def get_image(self, obj):
        crop = get_thumbnail(obj.product_image.image, '80x80', crop='center', quality=99)
        return crop.url

    def get_image_big(self, obj):
        crop = get_thumbnail(obj.product_image.image, '530x530', crop='center', quality=99)
        return crop.url


class ProductDetailSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    attribute_option = AttributeOptionFilterSerializer(many=True)

    class Meta:
        model = Product
        fields = ['price', 'product_image', 'attribute_option', 'stock', 'is_exhausted', 'sku']

    def get_product_image(self, obj):
        product_image = obj.product_product_images.all().order_by('is_featured')
        # product_image_featured = product_image.filter(is_featured=True)
        # if product_image_featured.exists():
        #     product_image_featured = product_image_featured.prefetch_related('product_image').first()
        # else:
        #     product_image_featured = product_image.prefetch_related('product_image').first()
        return ProductImageDetailSerializer(product_image, many=True).data


class ProductClassAttrSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    product_variant = serializers.SerializerMethodField()
    influencer_name = serializers.CharField(source='get_influencer_name', read_only=True)

    class Meta:
        model = ProductClass
        fields = ['name', 'slug', 'id', 'product_variant', 'description', 'influencer_name']


    def get_product_variant(self, obj):
        product_variant = obj.product_class_products.filter(is_active=True).order_by('is_featured')
        return ProductDetailSerializer(product_variant.first()).data


class ProductClassDetailSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    product_variant = serializers.SerializerMethodField()

    class Meta:
        model = ProductClass
        fields = ['product_variant']


    def get_product_variant(self, obj):
        product_variant = obj.product_class_products.filter(is_active=True).order_by('is_featured')
        return ProductDetailSerializer(product_variant.first()).data


class InfluencerFilterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Influencer
        fields = ['name', 'id', 'slug']

