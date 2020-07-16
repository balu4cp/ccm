from datetime import datetime, date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from common.mixins import ExceptionHandlerMixin, CustomPagination, PaginationHandlerMixin
from hub.serializers.request_management import (
    HubRequestsListSerializer,
    HubRequestDetailsSerializer,
    HubConvertToOrderDetailsSerializer,
    HubRequestStockStatusSerializer,
    HubConvertToOrderSerializer,
    HubMarkProcessedSerializer
)
from ffadmin.services.request_management import (
    get_requests_lists,
    get_requests_details,
    get_convert_order_details,
    check_request_stock_status,
    convert_to_order,
    mark_request_processed
)
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from common import utility
from common.permissions import HubViewRequestListPermission, HubManageRequestPermission


# Author Jose
class HubRequestListAPI(ExceptionHandlerMixin, APIView, PaginationHandlerMixin):
    """ API for getting list of UserRequests"""

    pagination_class = CustomPagination
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubViewRequestListPermission]

    def get(self, request):
        user = request.user
        search_term = request.query_params.get("search_term")
        list_size = request.query_params.get("list_size")
        if list_size in [None, '']:
            list_size = 10
        CustomPagination.page_size = list_size
        utility.log_save("API- RequestListAPI", "Get list of User Requests", user.username, "GENERAL")
        queryset = get_requests_lists(user, search_term)
        total_count = queryset.count()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = HubRequestsListSerializer(page, many=True)
            data = {
                "data": serializer.data,
                "total_count": total_count,
                "page_size": list_size,
            }
            return self.get_paginated_response(data)
        serializer = HubRequestsListSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# Author Jose
class HubRequestDetailsAPI(ExceptionHandlerMixin, APIView):
    """API for UserRequest Details """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubViewRequestListPermission]

    def get(self, request):
        user = request.user
        request_uid = request.query_params.get("request_uid")
        queryset = get_requests_details(user, request_uid)
        serializer = HubRequestDetailsSerializer(queryset)
        utility.log_save("API-HubRequestDetailsAPI", "Details fetched", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# Author Jose
class HubConvertToOrderDetailsAPI(ExceptionHandlerMixin, APIView):
    """API for getting details for Convert To Order Details page """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubManageRequestPermission]

    def get(self, request):
        user = request.user
        request_uid = request.query_params.get("request_uid")
        queryset = get_convert_order_details(user, request_uid)
        serializer = HubConvertToOrderDetailsSerializer(queryset)
        utility.log_save("API-HubConvertToOrderDetailsAPI", "Details fetched", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# Author Jose
class HubRequestStockStatusAPI(ExceptionHandlerMixin, APIView):
    """API for checking stock status of request sku """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubManageRequestPermission]

    def get(self, request):
        user = request.user
        request_uid = request.query_params.get("request_uid")
        queryset = check_request_stock_status(user, request_uid)
        serializer = HubRequestStockStatusSerializer(queryset)
        utility.log_save("API-HubConvertToOrderDetailsAPI", "Details fetched", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# Author Jose
class HubConvertToOrderAPI(ExceptionHandlerMixin, APIView):
    """API for converting UserRequest to Order"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubManageRequestPermission]

    def post(self, request):
        user = request.user
        serializer = HubConvertToOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        convert_to_order(user, **serializer.validated_data)
        utility.log_save("API-HubConvertToOrderAPI", "Converted to Order", user.username, "GENERAL")
        return Response(status=status.HTTP_201_CREATED, data="Converted to order successfully")


# Author Jose
class HubMarkRequestProcessedAPI(ExceptionHandlerMixin, APIView):
    """API for status change in DeliveryOrder detail page"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubManageRequestPermission]

    def post(self, request):
        user = request.user
        serializer = HubMarkProcessedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mark_request_processed(user, **serializer.validated_data)
        utility.log_save("API-HubMarkRequestProcessedAPI", "UserRequest marked processed", user.username, "GENERAL")
        return Response(status=status.HTTP_201_CREATED, data="UserRequest marked processed")
