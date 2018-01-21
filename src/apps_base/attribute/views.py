from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from apps_base.core.mixins import BaseAuthenticated
from .serializers import AttributeSerializer
from .models import Attribute

class AttributeViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = AttributeSerializer
    queryset = Attribute.objects.filter(is_trash=False)


