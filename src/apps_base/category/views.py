from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from apps_base.core.mixins import BaseAuthenticated
from apps_base.core.mixins import StandardPagination
from .serializers import CategorySerializer
from .models import Category


class CategoryViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_trash=False)
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        field = self.request.query_params.get('field', None)
        order_by = self.request.query_params.get('orderBy', None)
        category = self.request.query_params.get('category', False)
        search = self.request.query_params.get('search', None)
        is_category_parent = self.request.query_params.get('is_category_parent', False)
        if category:
            queryset = queryset.filter(category__isnull=True)
        if search:
            queryset = queryset.filter(name__icontains=search)
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
    queryset = Category.objects.filter(is_trash=False, category__isnull=True)
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', False)
        if category:
            queryset = queryset.exclude(id=int(category))

        return queryset
