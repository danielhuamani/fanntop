from django.conf.urls import url
from .views import influencer_products, category_products, category_child_products

urlpatterns = [
    url(r"^influenciador/(?P<slug>[\w-]+)/$", influencer_products, name="influencer_products"),
    url(r"^categoria/(?P<slug>[\w-]+)/$", category_products, name="category_products"),
    url(r"^categoria/(?P<slug>[\w-]+)/(?P<slug_child>[\w-]+)/$", category_child_products, name="category_child_products"),

]
