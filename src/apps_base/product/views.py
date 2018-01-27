from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from .models import ProductClass
from apps_base.core.mixins import BaseAuthenticated
from .serializers import ProductClassSerializer
from apps_base.attribute.serializers import AttributeSerializer
from apps_base.attribute.models import Attribute
from apps_base.family.models import Family, FamilyGroup, FamilyGroupAttribute

class ProductClassViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = ProductClass.objects.all()
    serializer_class = ProductClassSerializer

class ProductAttributeAPI(BaseAuthenticated, ListAPIView):
    queryset = Attribute.objects.filter(is_variation=True)
    serializer_class = AttributeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        family_id = self.request.query_params.getlist('family[]', None)
        attribute_ids = self.request.query_params.getlist('attribute_ids[]', None)
        if attribute_ids:
            queryset = queryset.filter(id__in=attribute_ids)
        elif family_id:
            attribute_ids = FamilyGroupAttribute.objects.filter(family_group__family__id__in=family_id)
            queryset = queryset.filter(id__in=list(attribute_ids.values_list('atribute_id', flat=True)))
        else:
            queryset = queryset.none()
        return queryset
