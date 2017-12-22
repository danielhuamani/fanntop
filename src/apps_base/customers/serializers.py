from .models import Customer
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['document', 'type_document', 'offers_news',
            'gender', 'terms_conditions', 'phone']
