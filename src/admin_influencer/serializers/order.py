from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from apps_base.product.models import Product, ProductImage
from sorl.thumbnail import get_thumbnail
from apps_base.order.models import Order, OrderCustomer, OrderDetail, OrderShippingAddress
from django.utils import timezone

class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()
    attrs = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product_name', 'product_image', 'attrs']

    def get_product_name(self, obj):
        return obj.product_class.name

    def get_product_image(self, obj):
        images = obj.product_product_images.all().first()
        crop = get_thumbnail(images.product_image.image, '80x80', crop='center', quality=99)
        return self.context['request'].build_absolute_uri(crop.url)

    def get_attrs(self, obj):
        return list(obj.attribute_option.all().values('option', 'attribute__name'))


class OrderDetailSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    # ubigeo_full = serializers.SerializerMethodField()
    productdetail = OrderProductSerializer()
    class Meta:
        model = OrderDetail
        fields = ['productdetail', 'quantity', 'sub_total', 'total', 'price']


class OrderShippingAddressSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    ubigeo_full = serializers.SerializerMethodField()

    class Meta:
        model = OrderShippingAddress
        fields = ['first_name', 'last_name', 'type_document', 'document', 'phone',
                'address', 'reference', 'ubigeo', 'ubigeo_full']

    def get_ubigeo_full(self, obj):
        return obj.ubigeo.full_ubigeo()


class OrderCustomerSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    # user = UserSerializer()
    # customer_shipping_address = CustomerShippingAddressSerializer(many=True)

    class Meta:
        model = OrderCustomer
        fields = ['first_name', 'last_name', 'email', 'phone', 'document', 'type_document']


class OrderSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    # user = UserSerializer()
    # customer_shipping_address = CustomerShippingAddressSerializer(many=True)
    order_order_customer = OrderCustomerSerializer()
    order_ordershipping = OrderShippingAddressSerializer()
    # order_orderdetail = OrderDetailSerializer(many=True)
    # order_orderdetail = OrderDetailSerializer(many=True)
    # influencer_subtotal = serializers.FloatField()
    # influencer_discount = serializers.FloatField()
    # influencer_total = serializers.FloatField()
    fecha = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()
    influencer_extra = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['code', 'order_order_customer',
            'order_ordershipping', 'details', 'id', 'is_send_email',
            'status', 'extra_data',
            'fecha', 'influencer_extra']

    def get_fecha(self, obj):
        return timezone.localtime(obj.created).strftime("%I:%M %p %d/%m/%Y ")
    # def get_total_discount(self, obj):
    #     influencer_id = self.context.get('influencer_id')
    #     print(influencer_id, 'shippingss', obj.shipping_influencer)
    #     try:
    #         shipping = obj.shipping_influencer.get(str(influencer_id))
    #         print(shipping, 'shipping')
    #         if shipping:
    #             return float(shipping['total'])
    #         return float(0)
    #     except Exception as e:
    #         return float(0)
    def get_influencer_extra(self, obj):
        influencer_id = self.context.get('influencer_id')
        return obj.shipping_influencer.get(str(influencer_id))

    def get_status(self, obj):
        return obj.get_type_status_shipping_display()

    def get_details(self, obj):
        influencer_id = self.context.get('influencer_id')
        detail = obj.order_orderdetail.filter(
            productdetail__product_class__influencer__id=influencer_id)
        return OrderDetailSerializer(detail, many=True, context=self.context).data