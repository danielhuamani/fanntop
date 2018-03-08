from django.conf.urls import url, include

urlpatterns = [
    url(r'^culqui/', include([
        url(r'',
            include('apps_base.payment.culqui.urls'))]))
]

