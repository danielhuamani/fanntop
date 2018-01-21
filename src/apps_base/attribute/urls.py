from django.conf.urls import url
from rest_framework import routers
from .views import AttributeViewSet

router = routers.SimpleRouter()
router.register(r'', AttributeViewSet)

urlpatterns = [
]

urlpatterns += router.urls