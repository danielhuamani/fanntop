from django.conf.urls import url
from rest_framework import routers
from .views import OrderViewSet, OrderDashboardHeaderAPI, OrderDashboardSalesAPI, OrderDashboardCountAPI

router = routers.SimpleRouter()
router.register(r'order', OrderViewSet)

urlpatterns = [
    url(r"^order-dashboard-header/$", OrderDashboardHeaderAPI.as_view()),
    url(r"^order-dashboard-sales/$", OrderDashboardSalesAPI.as_view()),
    url(r"^order-dashboard-count/$", OrderDashboardCountAPI.as_view()),
]

urlpatterns += router.urls