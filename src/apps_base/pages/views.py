from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from apps_base.core.mixins import BaseAuthenticated
from .serializers import HomeBannerSerializer, FrequentQuestionSerializer
from .models import HomeBanner, FrequentQuestion


class HomeBannerViewSet(BaseAuthenticated, viewsets.ModelViewSet):

    serializer_class = HomeBannerSerializer
    queryset = HomeBanner.objects.filter(is_trash=False)
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)


class FrequentQuestionAPI(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        frequent_question, created = FrequentQuestion.objects.get_or_create(pk=1)
        serializer = FrequentQuestionSerializer(frequent_question)
        return Response(serializer.data)

    def post(self, request, format=None):
        frequent_question, created = FrequentQuestion.objects.get_or_create(pk=1)
        serializer = FrequentQuestionSerializer(data=request.data, instance=frequent_question)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)