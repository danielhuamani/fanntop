from django.shortcuts import render
from rest_framework import viewsets
from apps_base.core.mixins import BaseAuthenticated
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Order.objects.all().prefetch_related('order_ordershipping',
        'order_ordershipping__ubigeo', 'order_orderdetail', 'order_order_customer',
        'order_orderdetail__productdetail',
        'order_orderdetail__productdetail__product_product_images__product_image')
    serializer_class = OrderSerializer

