from rest_framework import serializers
from .models import Suscription, Contact


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

