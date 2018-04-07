from django.conf.urls import url
from rest_framework import routers
from .views import (HomeBannerViewSet, TermsConditionsAPI, PaymentMethodsAPI,
    PagesViewSet, FrequentQuestionResponseSet)

router = routers.SimpleRouter()
router.register(r'home', HomeBannerViewSet)
router.register(r'pages', PagesViewSet)
router.register(r'frecuent-question', FrequentQuestionResponseSet)

urlpatterns = [
    url(r"^terms-conditions/$", TermsConditionsAPI.as_view(), name="terms_conditions"),
    url(r"^payment-methods/$", PaymentMethodsAPI.as_view(), name="payment_methods"),
]

urlpatterns += router.urls
