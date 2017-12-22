from django.conf.urls import url
from rest_framework import routers
from .views import CustomerViewSet

router = routers.SimpleRouter()
router.register(r'customers', CustomerViewSet)

urlpatterns = [

]

urlpatterns += router.urls