from django.conf.urls import url
from .views import save_token
urlpatterns = [
    url(r'^save-token/$', save_token, name='save_token'),
]

