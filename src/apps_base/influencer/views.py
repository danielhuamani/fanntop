from django.shortcuts import render
from rest_framework import viewsets
from .serializers import InfluencerSerializer
from .models import Influencer

class InfluencerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = InfluencerSerializer
    queryset = Influencer.objects.filter(is_trash=False)
