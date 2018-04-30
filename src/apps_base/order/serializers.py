from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from apps_base.product.models import Product, ProductImage
from sorl.thumbnail import get_thumbnail
from .models import Order, OrderCustomer, OrderDetail, OrderShippingAddress


class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product_name', 'product_image']

    def get_product_name(self, obj):
        return obj.product_class.name

    def get_product_image(self, obj):
        images = obj.product_product_images.all().first()
        crop = get_thumbnail(images.product_image.image, '80x80', crop='center', quality=99)
        return self.context['request'].build_absolute_uri(crop.url)

class OrderCustomerSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    # user = UserSerializer()
    # customer_shipping_address = CustomerShippingAddressSerializer(many=True)

    class Meta:
        model = OrderCustomer
        fields = ['first_name', 'last_name', 'email', 'phone', 'document', 'type_document']


class OrderShippingAddressSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    ubigeo_full = serializers.SerializerMethodField()

    class Meta:
        model = OrderShippingAddress
        fields = ['first_name', 'last_name', 'type_document', 'document', 'phone',
                'address', 'reference', 'ubigeo', 'ubigeo_full']

    def get_ubigeo_full(self, obj):
        return obj.ubigeo.full_ubigeo()


class OrderDetailSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    # ubigeo_full = serializers.SerializerMethodField()
    productdetail = OrderProductSerializer()
    class Meta:
        model = OrderDetail
        fields = ['productdetail', 'quantity', 'sub_total', 'total', 'price']

    # def get_ubigeo_full(self, obj):
    #     return obj.ubigeo.full_ubigeo()


class OrderSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    # user = UserSerializer()
    # customer_shipping_address = CustomerShippingAddressSerializer(many=True)
    status = serializers.SerializerMethodField()
    order_order_customer = OrderCustomerSerializer()
    order_ordershipping = OrderShippingAddressSerializer()
    order_orderdetail = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ['code', 'total', 'type_status', 'order_order_customer', 'status',
            'order_ordershipping', 'order_orderdetail', 'id', 'is_send_email',
            'shipping_influencer', 'type_status_shipping', 'extra_data', 'discount',
            'shipping_price', 'sub_total']

    def update(self, instance, validated_data):
        order_order_customer = validated_data.pop('order_order_customer')
        order_ordershipping = validated_data.pop('order_ordershipping')
        order_orderdetail = validated_data.pop('order_orderdetail')
        instance = super(OrderSerializer, self).update(instance, validated_data)
        return instance

    def get_status(self, obj):
        return obj.get_type_status_display()