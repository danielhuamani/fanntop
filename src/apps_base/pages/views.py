from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from apps_base.core.mixins import BaseAuthenticated
from .serializers import HomeBannerSerializer
from .models import HomeBanner


class HomeBannerViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = HomeBannerSerializer
    queryset = HomeBanner.objects.filter(is_trash=False)
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
