from django.conf.urls import url
from rest_framework import routers
from .views import HomeBannerViewSet

router = routers.SimpleRouter()
router.register(r'home', HomeBannerViewSet)

urlpatterns = [

]

urlpatterns += router.urls
