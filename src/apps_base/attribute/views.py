from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from apps_base.core.mixins import BaseAuthenticated
from rest_framework.generics import ListAPIView
from .serializers import AttributeSerializer, AttributeOptionSerializer
from .models import Attribute, AttributeOption


class AttributeViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = AttributeSerializer
    queryset = Attribute.objects.filter(is_trash=False)


class AttributeOptionViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = AttributeOptionSerializer
    queryset = AttributeOption.objects.filter(is_trash=False)


class AttributeOptionListAPI(BaseAuthenticated, ListAPIView):

    serializer_class = AttributeOptionSerializer
    queryset = AttributeOption.objects.all()

    def get_queryset(self):

        queryset = super().get_queryset()
        attribute_id = self.request.query_params.get('attribute_id')
        print(attribute_id, 'attribute_id')
        if attribute_id:
            queryset = queryset.filter(attribute_id=int(attribute_id))
        else:
            queryset.none()
        return queryset
