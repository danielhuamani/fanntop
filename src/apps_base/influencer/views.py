from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from apps_base.core.mixins import BaseAuthenticated
from apps_base.core.mixins import StandardPagination
from .serializers import InfluencerSerializer
from .models import Influencer

class InfluencerViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = InfluencerSerializer
    queryset = Influencer.objects.filter(is_trash=False)
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        field = self.request.query_params.get('field', None)
        order_by = self.request.query_params.get('orderBy', None)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(slug__icontains=search))
        if field:
            if order_by == 'asc':
                queryset = queryset.order_by(field)
            elif order_by == 'desc':
                queryset = queryset.order_by('-'+field)
        return queryset