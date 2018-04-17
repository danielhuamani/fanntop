from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from apps_base.customers.models import CustomerShippingAddress


class CustomerShippingAddressSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    departamento = serializers.SerializerMethodField()
    provincia = serializers.SerializerMethodField()

    class Meta:
        model = CustomerShippingAddress
        fields = [
            'first_name', 'last_name', 'type_document', 'document',
            'phone', 'address', 'reference', 'ubigeo', 'departamento', 'provincia'
        ]

    def get_departamento(self, obj):
        return obj.ubigeo.cod_dep_inei

    def get_provincia(self, obj):
        return obj.ubigeo.cod_prov_inei