from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from apps_base.custom_auth.constants import ECOMMERCE, INFLUENCER, ADMIN
# Create your views here.



class PermissionInfluencer(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated
        if is_authenticated:
            return request.user.type_user == INFLUENCER
        else:
            return False

class PermissionEcommerce(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated
        if is_authenticated:
            return request.user.type_user in [ECOMMERCE, ADMIN]
        else:
            return False

class BaseAuthenticated:
    authentication_classes = (SessionAuthentication, BasicAuthentication,
                                JSONWebTokenAuthentication)
    permission_classes = (PermissionEcommerce,)


class BaseInfluencerAuthenticated:
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (PermissionInfluencer,)


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000