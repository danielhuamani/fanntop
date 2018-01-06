from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from apps_base.core.mixins import BaseAuthenticated
from .serializers import CategorySerializer
from .models import Category

class CategoryViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_trash=False)
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def get_queryset(self):
        queryset = super().get_queryset()
        field = self.request.query_params.get('field', None)
        order_by = self.request.query_params.get('orderBy', None)
        category = self.request.query_params.get('category', False)
        is_category_parent = self.request.query_params.get('is_category_parent', False)
        if field:
            if order_by == 'asc':
                queryset = queryset.order_by(field)
            elif order_by == 'desc':
                queryset = queryset.order_by('-'+field)
        return queryset


class CategoryListAPI(BaseAuthenticated, ListCreateAPIView):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_trash=False)
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', False)
        if category:
            queryset = queryset.get(id=int(category)).category_categories.all()
        else:
            queryset = self.queryset.filter(category__isnull=True)
        return queryset