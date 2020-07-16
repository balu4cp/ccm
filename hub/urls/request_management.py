from django.urls import path
from hub.views.apis import api_requestmanagement

urlpatterns = [
    path("api/request/list/get", api_requestmanagement.HubRequestListAPI.as_view()),
    path("api/request/details/get", api_requestmanagement.HubRequestDetailsAPI.as_view()),
    path("api/request/convert/order/details/get", api_requestmanagement.HubConvertToOrderDetailsAPI.as_view()),
    path("api/request/check/stock/status", api_requestmanagement.HubRequestStockStatusAPI.as_view()),  
    path("api/request/convert/order", api_requestmanagement.HubConvertToOrderAPI.as_view()),  
    path("api/request/mark/processed", api_requestmanagement.HubMarkRequestProcessedAPI.as_view()),
]
