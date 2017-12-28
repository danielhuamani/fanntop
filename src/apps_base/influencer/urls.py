from django.conf.urls import url
from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token
from .views import InfluencerViewSet

router = routers.SimpleRouter()
router.register(r'', InfluencerViewSet)

urlpatterns = [

]

urlpatterns += router.urls