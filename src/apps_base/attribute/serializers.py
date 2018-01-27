from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from django.db import transaction
from .models import Attribute, AttributeOption
from .constants import COLOUR, SELECT_MULTIPLE, SELECT_SINGLE


class AttributeOptionSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = AttributeOption
        fields = [
            'id', 'attr', 'option'
        ]


class AttributeSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    attribute_options = AttributeOptionSerializer(many=True)

    class Meta:
        model = Attribute
        fields = [
            'id', 'name', 'name_store', 'is_use_search', 'type_name',
            'is_filter', 'is_variation', 'attribute_options'
        ]

    @transaction.atomic
    def create(self, validated_data):
        attribute_options = validated_data.pop('attribute_options')
        type_name = validated_data.get('type_name')
        attribute = Attribute.objects.create(**validated_data)
        if type_name in [COLOUR, SELECT_MULTIPLE, SELECT_SINGLE]:
            for attr in attribute_options:
                AttributeOption.objects.create(attribute=attribute, **attr)
        return attribute

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.name_store = validated_data.get('name_store', instance.name_store)
        instance.is_use_search = validated_data.get('is_use_search', instance.is_use_search)
        instance.type_name = validated_data.get('type_name', instance.type_name)
        instance.is_filter = validated_data.get('is_filter', instance.is_filter)
        instance.is_variation = validated_data.get('is_variation', instance.is_variation)
        instance.save()
        attribute_options = validated_data.pop('attribute_options')

        if attribute_options and instance.type_name in [COLOUR, SELECT_MULTIPLE, SELECT_SINGLE]:
            for attr in attribute_options:
                item_id = attr.get('id', None)
                if item_id:
                    attribute_option = AttributeOption.objects.get(id=item_id, attribute=instance)
                    attribute_option.attr = attr.get('attr', attribute_option.attr)
                    attribute_option.option = attr.get('attr', attribute_option.option)
                    attribute_option.save()
                else:
                    AttributeOption.objects.create(attribute=instance, **attr)
        return instance
