from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from apps_base.core.mixins import BaseAuthenticated
from .serializers import SuscriptionSerializer, ContactSerializer, ComplaintsBookSerializer
from .models import Suscription, Contact, ComplaintsBook


class SuscriptionViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = SuscriptionSerializer
    queryset = Suscription.objects.all()


class ContactViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


class ComplaintsBookViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = ComplaintsBookSerializer
    queryset = ComplaintsBook.objects.all()