from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from django.db import transaction
from .models import Family, FamilyGroup, FamilyAttribute
from apps_base.attribute.models import Attribute


class AttributeSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = [
            'id', 'name', 'name_store']


class FamilyAttributeSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    name_attr = serializers.SerializerMethodField()
    type_name = serializers.SerializerMethodField()
    is_variation = serializers.SerializerMethodField()

    class Meta:
        model = FamilyAttribute
        fields = [
            'id', 'attribute', 'is_required', 'position', 'name_attr',
            'type_name', 'is_variation', 'family'
        ]

    def get_name_attr(self, obj):
        return obj.attribute.name

    def get_type_name(self, obj):
        return obj.attribute.type_name

    def get_is_variation(self, obj):
        return obj.attribute.is_variation


class FamilyGroupSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    familygroup_familygroupatribute = FamilyAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = FamilyGroup
        fields = [
            'id', 'name', 'family', 'position' , 'familygroup_familygroupatribute'
        ]


class FamilySerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Family
        fields = [
            'id', 'name', 'is_active'
        ]
