from rest_framework import serializers
from apps_base.form.models import Suscription


class SuscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscription
        fields = ['email']
