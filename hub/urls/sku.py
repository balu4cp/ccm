from django.urls import path
from hub.views.apis import api_sku

urlpatterns = [
    path("api/sku/list/get", api_sku.HubSKUListView.as_view()),
    path("api/sku/detail/get", api_sku.HubSkuDetailGetAPI.as_view()),
    path("api/sku/create", api_sku.HubSkuCreateAPI.as_view()),
    path("api/sku/update", api_sku.HubSkuUpdateAPI.as_view()),
    path("api/sku/status/toggle", api_sku.HubSKUStatusChangeView.as_view()),
]
