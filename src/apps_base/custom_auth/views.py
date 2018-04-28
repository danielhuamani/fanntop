from django.shortcuts import render
from rest_framework import viewsets
from apps_base.core.mixins import BaseAuthenticated
from .models import User
from .serializers import UserSerializer


class UserViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer