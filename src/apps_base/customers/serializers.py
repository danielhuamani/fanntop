from .models import Customer, CustomerShippingAddress
from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from apps_base.custom_auth.serializers import UserSerializer


class CustomerShippingAddressSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    ubigeo_full = serializers.SerializerMethodField()

    class Meta:
        model = CustomerShippingAddress
        fields = ['first_name', 'last_name', 'type_document', 'document', 'phone',
                'address', 'reference', 'ubigeo', 'ubigeo_full']

    def get_ubigeo_full(self, obj):
        return obj.ubigeo.full_ubigeo()

class CustomerSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    user = UserSerializer()
    customer_shipping_address = CustomerShippingAddressSerializer(many=True)

    class Meta:
        model = Customer
        fields = ['document', 'type_document', 'is_offers_news',
            'gender', 'terms_conditions', 'phone', 'user', 'id', 'is_send_email',
            'customer_shipping_address']
