from django.shortcuts import render
from .serializers import UserJSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView


class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.
    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = UserJSONWebTokenSerializer


obtain_jwt_token = ObtainJSONWebToken.as_view()
