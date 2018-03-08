from django.conf.urls import url
from .views import departamentos, provincias, distritos

urlpatterns = [
    url(r'^departamentos/$', departamentos, name='api_departamentos'),
    url(r'^provincias/$', provincias, name='api_provincias'),
    url(r'^distritos/$', distritos, name='api_distritos'),
]
