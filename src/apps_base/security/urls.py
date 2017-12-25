from django.conf.urls import url
from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token
from .views import obtain_jwt_token
# router = routers.SimpleRouter()
# router.register(r'customers', CustomerViewSet)

urlpatterns = [
    url(r'token-auth/', obtain_jwt_token),
    url(r'token-refresh/', refresh_jwt_token),
    url(r'token-verify/', verify_jwt_token),
]

