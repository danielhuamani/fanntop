from django.shortcuts import render
from rest_framework import viewsets
from apps_base.core.mixins import BaseAuthenticated
from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer