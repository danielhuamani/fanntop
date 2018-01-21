from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from django.db import transaction
from .models import Family, FamilyGroup, FamilyGroupAttribute
from apps_base.attribute.models import Attribute


class FamilySerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Family
        fields = [
            'id', 'name', 'is_active'
        ]


class AttributeSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = [
            'id', 'name', 'name_store']


class FamilyGroupAttributeSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = FamilyGroupAttribute
        fields = [
            'id', 'family_group', 'atribute', 'is_required', 'position'
        ]


class FamilyGroupSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = FamilyGroup
        fields = [
            'id', 'name', 'family', 'position'
        ]





