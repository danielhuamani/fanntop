from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from apps_base.core.mixins import BaseAuthenticated
from rest_framework.generics import ListCreateAPIView
from .serializers import (FamilySerializer, AttributeSerializer,
    FamilyGroupAttributeSerializer, FamilyGroupSerializer)
from apps_base.attribute.models import Attribute
from .models import Family, FamilyGroup, FamilyGroupAttribute


class FamilyViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = FamilySerializer
    queryset = Family.objects.filter(is_trash=False)


class FamilyGroupViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = FamilyGroupSerializer
    queryset = FamilyGroup.objects.all().order_by('position')

    def get_queryset(self):
        queryset = super().get_queryset()
        family = self.request.query_params.get('family', False)
        print("entras")
        if family:
            queryset = queryset.filter(family_id=int(family))
        return queryset

class FamilyGroupAttributeViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = FamilyGroupAttributeSerializer
    queryset = FamilyGroupAttribute.objects.filter(is_trash=False)



class AttributeListAPI(BaseAuthenticated, ListCreateAPIView):

    serializer_class = AttributeSerializer
    queryset = Attribute.objects.filter(is_trash=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        family_group = self.request.query_params.get('family_group', False)
        if family_group:
            family_id = FamilyGroup.objects.get(id=int(family_group)).family_id
            family_group_attr = FamilyGroupAttribute.objects.filter(family_group__family__id=int(family_id)).values_list('atribute_id', flat=True)
            queryset = queryset.exclude(id__in=list(family_group_attr))
        return queryset
