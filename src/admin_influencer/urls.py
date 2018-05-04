from django.conf.urls import url
from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token
from .api_views import (obtain_jwt_token, ProductListAPI, ProductDetailAPI,
    OrderListAPI, OrderDetailAPI, UserAPI, UserChangePassAPI)
# router = routers.SimpleRouter()
# router.register(r'customers', CustomerViewSet)

urlpatterns = [
    url(r'^token-auth/$', obtain_jwt_token),
    url(r'^product/$', ProductListAPI.as_view()),
    url(r'^product/(?P<slug>[\w-]+)/$', ProductDetailAPI.as_view()),
    url(r'^order/$', OrderListAPI.as_view()),
    url(r'^order/(?P<code>[\w-]+)/$', OrderDetailAPI.as_view()),
    url(r'^user/$', UserAPI.as_view()),
    url(r'^user-change-pass/$', UserChangePassAPI.as_view())
]

