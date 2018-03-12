from django.conf.urls import url
from rest_framework import routers
from .views import HomeBannerViewSet, FrequentQuestionAPI

router = routers.SimpleRouter()
router.register(r'home', HomeBannerViewSet)

urlpatterns = [
    url(r"^question/$", FrequentQuestionAPI.as_view(), name="question"),
]

urlpatterns += router.urls
