from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
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
        if field:
            if order_by == 'asc':
                queryset = queryset.order_by(field)
            elif order_by == 'desc':
                queryset = queryset.order_by('-'+field)
        return queryset