from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
]  + (
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

urlpatterns += [
    url(r'^api-v1/', include([
        url(r'security/',
            include('apps_base.security.urls', namespace='security')),
        url(r'influencer/',
            include('apps_base.influencer.urls', namespace='influencer')),
        url(r'category/',
            include('apps_base.category.urls', namespace='category')),
        url(r'product/',
            include('apps_base.product.urls', namespace='product')),
        url(r'family/',
                include('apps_base.family.urls', namespace='family')),
        url(r'attribute/',
            include('apps_base.attribute.urls', namespace='attribute')),
        url(r'pages/',
            include('apps_base.pages.urls', namespace='pages')),
        url(r'ubigeo/', include('apps_base.ubigeo.urls', namespace='ubigeo')),
        url(r'payment/', include('apps_base.payment.urls', namespace='payment'))
    ])),
    url(r'^', include('apps_web.web_system.urls', namespace='web_system')),
    url(r'^', include('apps_web.web_product.urls', namespace='web_product')),
    url(r'^', include('apps_web.web_cart.urls', namespace='web_cart')),
    url(r'^', include('apps_web.web_order.urls', namespace='web_order')),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns