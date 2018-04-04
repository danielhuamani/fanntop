from django.shortcuts import render
from rest_framework import viewsets
from apps_base.core.mixins import BaseAuthenticated
from .models import Coupon, CouponGenerate
from .serializers import CouponSerializer, CouponGenerateSerializer


class CouponViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer



class CouponGenerateViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = CouponGenerate.objects.all().prefetch_related('customer', 'customer__user')
    serializer_class = CouponGenerateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        coupon_id = self.request.query_params.get('coupon_id', None)
        if coupon_id:
            queryset = queryset.filter(coupon_id=coupon_id)
        else:
            queryset = queryset.none()
        return queryset