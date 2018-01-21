from django.shortcuts import render
from rest_framework import viewsets
from .models import ProductClass
from .serializers import ProductClassSerializer


class ProductClassViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = ProductClass.objects.all()
    serializer_class = ProductClassSerializer