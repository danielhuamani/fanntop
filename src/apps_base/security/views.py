from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from apps_base.core.mixins import BaseAuthenticated
from .serializers import UserJSONWebTokenSerializer, UserProfileSerializer, UserChangePassSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView


class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.
    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = UserJSONWebTokenSerializer


obtain_jwt_token = ObtainJSONWebToken.as_view()


class UserAPI(BaseAuthenticated, RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        user = self.request.user
        return user


class UserChangePassAPI(BaseAuthenticated, UpdateAPIView):
    serializer_class = UserChangePassSerializer

    def get_object(self):
        user = self.request.user
        return user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("password")):
                return Response({"password": ["Wrong password."]}, status=403)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({}, status=200)

        return Response(serializer.errors, status=403)


