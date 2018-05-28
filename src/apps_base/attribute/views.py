from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from apps_base.core.mixins import BaseAuthenticated
from rest_framework.generics import ListAPIView
from .serializers import AttributeSerializer, AttributeOptionSerializer
from apps_base.core.mixins import StandardPagination
from .models import Attribute, AttributeOption


class AttributeViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = AttributeSerializer
    queryset = Attribute.objects.filter(is_trash=False)
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
