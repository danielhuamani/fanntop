from django.conf.urls import url
from rest_framework import routers
from .views import CategoryViewSet, CategoryListAPI

router = routers.SimpleRouter()
router.register(r'category', CategoryViewSet)

urlpatterns = [
    url(r"^category_list/$", CategoryListAPI.as_view(), name="category_list")
]

urlpatterns += router.urls