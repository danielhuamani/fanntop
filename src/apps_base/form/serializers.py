from rest_framework import serializers
from .models import Suscription


class SuscriptionSerializer(serializers.ModelSerializer):
    creation = serializers.SerializerMethodField()
    class Meta:
        model = Suscription
        fields = ['email', 'creation']

    def get_creation(self, obj):
        return obj.created.strftime("%H:%M %d/%m/%Y ")

