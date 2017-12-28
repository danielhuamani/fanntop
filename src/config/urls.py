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
            include('apps_base.influencer.urls', namespace='influencer'))
    ])),
    url(r'^', include('apps_web.web_system.urls', namespace='web_system'))
]