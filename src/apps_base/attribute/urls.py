from django.conf.urls import url
from rest_framework import routers
from .views import AttributeViewSet, AttributeOptionListAPI

router = routers.SimpleRouter()
router.register(r'attribute', AttributeViewSet)

urlpatterns = [
    url(r"^attribute_option_list/$", AttributeOptionListAPI.as_view(), name="attribute_option_list")
]

urlpatterns += router.urls
