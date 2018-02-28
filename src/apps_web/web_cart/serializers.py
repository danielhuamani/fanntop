from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from sorl.thumbnail import get_thumbnail
from apps_base.cart.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_sku = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'quantity', 'cart_item_total', 'product_price', 'image', 'product_name',
            'product_sku'
        ]

    def get_product_price(self, obj):
        return obj.product.get_price

    def get_product_name(self, obj):
        return obj.product.product_class.name

    def get_product_sku(self, obj):
        return obj.product.sku

    def get_image(self, obj):
        crop = get_thumbnail(obj.product.product_product_images.order_by('-is_featured').first().product_image.image, '60x60', crop='center', quality=99)
        return crop.url

class CartSerializer(serializers.ModelSerializer):
    # TODO: Define serializer fields here
    cart_items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = [
            'total', 'cart_items'
        ]
