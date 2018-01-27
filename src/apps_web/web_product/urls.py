from django.conf.urls import url
from .views import influencer_products

urlpatterns = [
    url(r"^influenciador/(?P<pk>\d+)/$", influencer_products, name="influencer_products"),
]
