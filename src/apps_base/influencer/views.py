from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from apps_base.core.mixins import BaseAuthenticated
from .serializers import InfluencerSerializer
from .models import Influencer

class InfluencerViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = InfluencerSerializer
    queryset = Influencer.objects.filter(is_trash=False)
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