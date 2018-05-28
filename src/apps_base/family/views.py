from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from apps_base.core.mixins import BaseAuthenticated
from rest_framework.generics import ListCreateAPIView
from .serializers import (FamilySerializer, AttributeSerializer,
    FamilyAttributeSerializer, FamilyGroupSerializer)
from apps_base.attribute.models import Attribute
from apps_base.core.mixins import StandardPagination
from .models import Family, FamilyGroup, FamilyAttribute


class FamilyViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = FamilySerializer
    queryset = Family.objects.filter(is_trash=False)
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        field = self.request.query_params.get('field', None)
        order_by = self.request.query_params.get('orderBy', None)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        if field:
            if order_by == 'asc':
                queryset = queryset.order_by(field)
            elif order_by == 'desc':
                queryset = queryset.order_by('-'+field)
        return queryset


class FamilyGroupViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = FamilyGroupSerializer
    queryset = FamilyGroup.objects.all().order_by('position')

    def get_queryset(self):
        queryset = super().get_queryset()
        family = self.request.query_params.get('family', False)
        if family:
            queryset = queryset.filter(family_id=int(family))
        return queryset

class FamilyAttributeViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = FamilyAttributeSerializer
    queryset = FamilyAttribute.objects.filter(is_trash=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        family_id = self.request.query_params.get('family_id', False)
        if family_id:
            queryset = queryset.filter(family_id=int(family_id))
        return queryset


class AttributeListAPI(BaseAuthenticated, ListCreateAPIView):

    serializer_class = AttributeSerializer
    queryset = Attribute.objects.filter(is_trash=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        family_id = self.request.query_params.get('family_id', False)
        attr_id = self.request.query_params.get('attr_id', False)
        if family_id:
            family_attribute = FamilyAttribute.objects.filter(family_id=int(family_id))
            if attr_id:
                family_attribute = family_attribute.exclude(attribute_id=int(attr_id))
            family_attribute = family_attribute.values_list('attribute_id', flat=True)
            queryset = queryset.exclude(id__in=list(family_attribute))
        return queryset
