from django.shortcuts import render
from rest_framework import viewsets, status
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from apps_base.core.mixins import BaseAuthenticated
from apps_base.core.mixins import StandardPagination
from .serializers import SuscriptionSerializer, ContactSerializer, ComplaintsBookSerializer
from .models import Suscription, Contact, ComplaintsBook


class SuscriptionViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = SuscriptionSerializer
    queryset = Suscription.objects.all()
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        field = self.request.query_params.get('field', None)
        order_by = self.request.query_params.get('orderBy', None)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(email__icontains=search)
        if field:
            if order_by == 'asc':
                queryset = queryset.order_by(field)
            elif order_by == 'desc':
                queryset = queryset.order_by('-'+field)
        return queryset


class ContactViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        field = self.request.query_params.get('field', None)
        order_by = self.request.query_params.get('orderBy', None)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(subject__icontains=search)
            )
        if field:
            if order_by == 'asc':
                queryset = queryset.order_by(field)
            elif order_by == 'desc':
                queryset = queryset.order_by('-'+field)
        return queryset


class ComplaintsBookViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = ComplaintsBookSerializer
    queryset = ComplaintsBook.objects.all()
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        field = self.request.query_params.get('field', None)
        order_by = self.request.query_params.get('orderBy', None)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        if field:
            if order_by == 'asc':
                queryset = queryset.order_by(field)
            elif order_by == 'desc':
                queryset = queryset.order_by('-'+field)
        return queryset
