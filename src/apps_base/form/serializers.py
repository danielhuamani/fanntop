from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from .models import Suscription, Contact, ComplaintsBook


class SuscriptionSerializer(serializers.ModelSerializer):
    creation = serializers.SerializerMethodField()
    class Meta:
        model = Suscription
        fields = ['email', 'creation']

    def get_creation(self, obj):
        return obj.created.strftime("%H:%M %d/%m/%Y ")


class ContactSerializer(serializers.ModelSerializer):
    creation = serializers.SerializerMethodField()
    class Meta:
        model = Contact
        fields = ['email', 'creation', 'first_name', 'last_name', 'subject', 'message']

    def get_creation(self, obj):
        return obj.created.strftime("%H:%M %d/%m/%Y ")


class ComplaintsBookSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    creation = serializers.SerializerMethodField()
    class Meta:
        model = ComplaintsBook
        fields = ['email', 'creation', 'first_name', 'last_name', 'id', 'document',
        'type_document', 'phone', 'ubigeo', 'address', 'type_claim', 'detail', 'pedido',
        'well_contracted', 'desciption', 'mount', 'consumers_order', 'observation', 'uuid']

    def get_creation(self, obj):
        return obj.created.strftime("%H:%M %d/%m/%Y ")

