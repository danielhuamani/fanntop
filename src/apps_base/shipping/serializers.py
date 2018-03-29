from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from .models import ShippingCost


class ShippingCostSerializer(serializers.ModelSerializer):
    full_ubigeo = serializers.SerializerMethodField()

    class Meta:
        model = ShippingCost
        fields = ['ubigeo', 'price', 'full_ubigeo', 'id']

    def get_full_ubigeo(self, obj):
        return obj.ubigeo.full_ubigeo()