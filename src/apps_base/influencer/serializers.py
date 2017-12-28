from rest_framework import serializers
from .models import Influencer, InfluencerSeo


class InfluencerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Influencer
        fields = [
            'id', 'name', 'description', 'image', 'position',
            'is_active', 'title', 'description', 'url'
        ]


class InfluencerSeoSerializer(serializers.ModelSerializer):

    class Meta:
        model = InfluencerSeo
        fields = ['id', 'title', 'description', 'url']