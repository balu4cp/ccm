from django.urls import path
from hub.views.apis import api_stockmanagement

urlpatterns = [
    path("api/sku/organization/stock/list/get", api_stockmanagement.HubOrganizationStockInfoListAPI.as_view()),
]
