from django.conf.urls import url
from .views import influencer_products, category_products, category_child_products, product, product_favorites
from .api_views import (ProductClassListAPI, CategoryFilterAPI, ProductClassCategoryListAPI,
    ProductClassListAPI, ProductClassAttrAPI, InfluencerFilterAPI,
    ProductClassInfluencerListAPI, ProductClassDetailAPI, CustomerProductFavoriteAPI)

urlpatterns = [
    url(r"^influenciador/(?P<slug>[\w-]+)/$", influencer_products, name="influencer_products"),
    url(r"^categoria/(?P<slug>[\w-]+)/$", category_products, name="category_products"),
    url(r"^categoria/(?P<slug>[\w-]+)/(?P<slug_child>[\w-]+)/$", category_child_products, name="category_child_products"),
    url(r"^producto/(?P<slug>[\w-]+)/$", product, name="product"),
    url(r"^mis-favoritos/$", product_favorites, name="product_favorites"),
    #  API
    url(r"^api/product-category/(?P<slug>[\w-]+)/(?P<slug_child>[\w-]+)/$", ProductClassCategoryListAPI.as_view(), name="product_class_category_list_api"),
    url(r"^api/product-influencer/(?P<slug>[\w-]+)/$", ProductClassInfluencerListAPI.as_view(), name="product_class_influencer_list_api"),
    url(r"^api/product/$", ProductClassListAPI.as_view(), name="product_class_list_api"),
    url(r"^api/product/(?P<slug>[\w-]+)/$", ProductClassAttrAPI.as_view(), name="product_class_attr_api"),
    url(r"^api/product-detail/(?P<slug>[\w-]+)/$", ProductClassDetailAPI.as_view(), name="product_class_detail_api"),
    url(r"^api/category-filter/(?P<slug>[\w-]+)/(?P<slug_child>[\w-]+)/$", CategoryFilterAPI.as_view(), name="category_filter"),
    url(r"^api/influencer-filter/(?P<slug>[\w-]+)/$", InfluencerFilterAPI.as_view(), name="influencer_filter"),
    url(r"^api/product-favorite/$", CustomerProductFavoriteAPI.as_view(), name="product_favorite")
]

