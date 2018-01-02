from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# Create your views here.


class BaseAuthenticated:
    authentication_classes = (SessionAuthentication, BasicAuthentication,
                                JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)