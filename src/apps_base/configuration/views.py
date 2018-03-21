from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ConfigurationSerializer
from .models import Configuration


class ConfigurationAPI(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        configuration, created = Configuration.objects.get_or_create(pk=1)
        serializer = ConfigurationSerializer(configuration)
        return Response(serializer.data)

    def post(self, request, format=None):
        configuration, created = Configuration.objects.get_or_create(pk=1)
        serializer = ConfigurationSerializer(data=request.data, instance=configuration)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
