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
    name_attr = serializers.SerializerMethodField()
    class Meta:
        model = FamilyGroupAttribute
        fields = [
            'id', 'family_group', 'atribute', 'is_required', 'position', 'name_attr'
        ]

    def get_name_attr(self, obj):
        return obj.atribute.name


class FamilyGroupSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    familygroup_familygroupatribute = FamilyGroupAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = FamilyGroup
        fields = [
            'id', 'name', 'family', 'position' , 'familygroup_familygroupatribute'
        ]
