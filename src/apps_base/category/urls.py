from django.conf.urls import url
from rest_framework import routers
from .views import CategoryViewSet

router = routers.SimpleRouter()
router.register(r'', CategoryViewSet)

urlpatterns = [

]

urlpatterns += router.urls