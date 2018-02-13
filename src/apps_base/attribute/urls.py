from django.conf.urls import url
from rest_framework import routers
from .views import AttributeViewSet, AttributeOptionListAPI, AttributeOptionViewSet

router = routers.SimpleRouter()
router.register(r'attribute', AttributeViewSet)
router.register(r'attribute-option', AttributeOptionViewSet)

urlpatterns = [
    url(r"^attribute_option_list/$", AttributeOptionListAPI.as_view(), name="attribute_option_list")
]

urlpatterns += router.urls
