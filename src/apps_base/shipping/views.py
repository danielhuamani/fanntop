from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import mixins
from .models import ShippingCost
from apps_base.core.mixins import BaseAuthenticated
from .serializers import ShippingCostSerializer



class ShippingCostViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = ShippingCost.objects.all().select_related('ubigeo')
    serializer_class = ShippingCostSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        provincia = self.request.query_params.get('provincia', None)
        get_distritos = self.request.query_params.get('get_distritos', None)
        field = self.request.query_params.get('field', None)
        order_by = self.request.query_params.get('orderBy', None)
        search = self.request.query_params.get('search', None)
        if get_distritos:
            if provincia:
                if search:
                    queryset = queryset.filter(ubigeo__desc_ubigeo_inei__icontains=search)
                if field:
                    if order_by == 'asc':
                        queryset = queryset.order_by(field)
                    elif order_by == 'desc':
                        queryset = queryset.order_by('-'+field)
                queryset = queryset.filter(ubigeo__cod_ubigeo_inei__startswith=provincia)
            return queryset
        else:
            queryset = queryset.none()
        return queryset
