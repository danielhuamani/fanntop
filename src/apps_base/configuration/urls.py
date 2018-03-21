from django.conf.urls import url
from rest_framework import routers
from .views import (ConfigurationAPI,)


urlpatterns = [
    url(r"^configuration/$", ConfigurationAPI.as_view(), name="configuration"),
]

