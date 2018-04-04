from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from django.db import transaction
from .models import Coupon, CouponGenerate
from .utils import generate_code_coupon


class CouponGenerateSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    client = serializers.SerializerMethodField()

    class Meta:
        model = CouponGenerate
        fields = ['code', 'is_used', 'date_validated', 'client']

    def get_client(self, obj):
        if obj.customer:
            return obj.customer.user.get_full_name()
        else:
            return ''

class CouponSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    quantity_generate = serializers.IntegerField(required=False)

    class Meta:
        model = Coupon
        fields = ['name', 'influencers', 'is_limit', 'date_start', 'date_end',
            'prefix', 'type_discount', 'discount', 'quantity_customer', 'quantity_generate', 'id',
            'is_active']

    @transaction.atomic
    def create(self, validated_data):
        print(validated_data, 'validated_data')
        quantity_generate = validated_data.pop('quantity_generate')
        coupon = super(CouponSerializer, self).create(validated_data)
        generate_code_coupon(coupon, quantity_generate)
        return coupon