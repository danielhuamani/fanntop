from django.conf.urls import url
from rest_framework import routers
from .views import (FamilyViewSet, AttributeListAPI,
    FamilyGroupViewSet, FamilyGroupAttributeViewSet)

router = routers.SimpleRouter()
router.register(r'family', FamilyViewSet)
router.register(r'family-group', FamilyGroupViewSet)
router.register(r'family-group-attribute', FamilyGroupAttributeViewSet)

urlpatterns = [
    url(r"^family_attribute/$", AttributeListAPI.as_view(), name="family_attribute")
]

urlpatterns += router.urls
