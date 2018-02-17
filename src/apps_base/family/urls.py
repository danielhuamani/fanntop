from django.conf.urls import url
from rest_framework import routers
from .views import (FamilyViewSet, AttributeListAPI,
    FamilyGroupViewSet, FamilyAttributeViewSet)

router = routers.SimpleRouter()
router.register(r'family', FamilyViewSet)
router.register(r'family-group', FamilyGroupViewSet)
router.register(r'family-attribute', FamilyAttributeViewSet)

urlpatterns = [
    url(r"^family_attribute/$", AttributeListAPI.as_view(), name="family_attribute")
]

urlpatterns += router.urls
