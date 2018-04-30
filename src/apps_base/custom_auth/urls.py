from django.conf.urls import url
from rest_framework import routers
from .views import UserViewSet, UserPasswordUpdate

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r"^user-password/(?P<pk>\d+)/$", UserPasswordUpdate.as_view(), name="user_password"),
]

urlpatterns += router.urls