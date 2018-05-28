from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView
from apps_base.core.mixins import BaseAuthenticated
from apps_base.core.mixins import StandardPagination
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserPasswordSerializer


class UserViewSet(BaseAuthenticated, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        print('rest')
        serializer = UserSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class UserPasswordUpdate(BaseAuthenticated, UpdateAPIView):
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        self.object = self.get_object()
        serializer = UserPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            self.object.set_password(serializer.data.get("confirm_password"))
            self.object.save()
            return Response(serializer.data)
        return Response(serializer.errors, 403)