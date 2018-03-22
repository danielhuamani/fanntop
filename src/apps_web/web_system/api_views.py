from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView
from .serializers import SuscriptionSerializer


class SuscriptionAPI(CreateAPIView):
    serializer_class = SuscriptionSerializer
