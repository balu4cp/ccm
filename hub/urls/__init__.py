from django.conf.urls import url, include

urlpatterns = [
    url("", include("hub.urls.site")),
    url("", include("hub.urls.usermanagement")),
    url("", include("hub.urls.roles")),
    url("", include("hub.urls.organisationmanagement")),
    url("", include("hub.urls.producer")),
    url("", include("hub.urls.sku")),
    url("", include("hub.urls.routing")),
    url("", include("hub.urls.request_management")),
    url("", include("hub.urls.stock_management")),
]