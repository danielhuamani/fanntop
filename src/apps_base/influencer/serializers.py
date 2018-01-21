from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from .models import Influencer


class InfluencerSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Influencer
        fields = [
            'id', 'name', 'description', 'image', 'position',
            'is_active', 'title', 'description', 'slug'
        ]

