from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.mixins import ExceptionHandlerMixin
from django.http import HttpResponseRedirect
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from common.mixins import (
    ExceptionHandlerMixin,
    PaginationHandlerMixin,
    CustomPagination,
)
from hub.serializers.producer import (
    ProducersListGetSerializer,
    ProducerDetailsGetSerializer,
    SKUListGetSerializer,
    SKUDetailSerializer,
    PredicedStockSerializer,
    ProducerSKUProcurementListSerializer,
    ProducerImageListSerializer,
    ProducerVideoListSerializer,
)
from common.permissions import HubViewSKUPermission, HubViewProducerPermission

from ffadmin.services.producer import (
    get_producer_list,
    get_sku_list,
    get_producersku_details,
    get_producer_sku_predicted_stock_list,
    get_producer_details,
    get_producerskuprocurement_list,
    get_producer_images,
    get_producer_videos,
)
from common import utility


class HubProducerListAPI(ExceptionHandlerMixin, APIView, PaginationHandlerMixin):
    """API for getting producers list View in hub"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubViewProducerPermission]
    pagination_class = CustomPagination

    def get(self, request):
        logged_user = request.user
        search_term = request.query_params.get("search_term")
        list_size = request.query_params.get("list_size")
        CustomPagination.page_size = list_size
        producers = get_producer_list(
            logged_user=logged_user, franchisee_id=None, list_size=list_size, search_term=search_term,
        )
        total_count = producers.count()
        page = self.paginate_queryset(producers)
        if page is not None:
            serializer = ProducersListGetSerializer(page, many=True)
            data = {
                "data": serializer.data,
                "total_count": total_count,
                "page_size": list_size,
            }
            utility.log_save("HubProducerListAPI", "Hub-pruducer list fetched", logged_user.username, "GENERAL")
            return self.get_paginated_response(data)
        serializer = ProducersListGetSerializer(producers, many=True)
        utility.log_save("HubProducerListAPI", "Hub-producer list fetched", logged_user.username, "GENERAL")
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class HubProducerDetailsGetAPI(ExceptionHandlerMixin, APIView):
    """API to get Producer details"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubViewProducerPermission]

    def get(self, request):
        user = request.user
        producer_id = request.query_params.get("producer_id")
        details = get_producer_details(producer_id, user)
        serializer = ProducerDetailsGetSerializer(details)
        utility.log_save("HubProducerDetailsGetAPI", "Hub-producer details fetched", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class HubProducerSKUListGetAPI(ExceptionHandlerMixin, APIView, PaginationHandlerMixin):
    """API for getting sku list of the producer"""

    pagination_class = CustomPagination
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubViewSKUPermission]

    def get(self, request):
        list_size = request.query_params.get("list_size")
        if list_size in [None, ""]:
            list_size = 10
        search_term = request.query_params.get("search_term")
        producer_id = request.query_params.get("producer_id")
        CustomPagination.page_size = list_size
        queryset = get_sku_list(request.user, producer_id=producer_id, list_size=list_size, search_term=search_term)
        total_count = queryset.count()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serialier = SKUListGetSerializer(page, many=True)
            data = {"data": serialier.data, "total_count": total_count, "page_size": list_size}
            utility.log_save(
                "HubProducerSKUListGetAPI", "Hub-producer sku list fetched", request.user.username, "GENERAL"
            )
            return self.get_paginated_response(data)
        serializer = SKUListGetSerializer(queryset, many=True)
        utility.log_save("HubProducerSKUListGetAPI", "Hub-producer sku list fetched", request.user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class HubProducerSKUDetailGetAPI(ExceptionHandlerMixin, APIView):
    """API to get Producer details"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubViewSKUPermission]

    def get(self, request):
        user = request.user
        producer_uid = request.query_params.get("producer_id")
        sku_uid = request.query_params.get("sku_uid")
        details = get_producersku_details(user, producer_uid, sku_uid)
        serializer = SKUDetailSerializer(details)
        utility.log_save("HubProducerSKUDetailGetAPI", "Hub-producer sku details fetched", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class HubPredictedStockListtGetAPI(ExceptionHandlerMixin, APIView, PaginationHandlerMixin):
    """API for getting predicted stock list of the producer"""

    pagination_class = CustomPagination
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubViewSKUPermission]

    def get(self, request):
        logged_user = request.user
        product_sku_id = request.query_params.get("product_sku_id")
        queryset = get_producer_sku_predicted_stock_list(logged_user, product_sku_id)
        serializer = PredicedStockSerializer(queryset, many=True)
        utility.log_save(
            "HubPredictedStockListtGetAPI", "Hub-producer predictedstock list fetched", logged_user.username, "GENERAL"
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# Jose
class HubProducerSKUProcurementListAPI(ExceptionHandlerMixin, APIView, PaginationHandlerMixin):
    """API for getting SKUProcurement list for Hub"""

    pagination_class = CustomPagination
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubViewProducerPermission]

    def get(self, request):
        user = request.user
        list_size = request.query_params.get("list_size")
        if list_size in [None, ""]:
            list_size = 10
        search_term = request.query_params.get("search_term")
        producer_uid = request.query_params.get("producer_uid")
        CustomPagination.page_size = list_size
        utility.log_save("API- HubProducerSKUProcurementListAPI", "List fetched", user.username, "GENERAL")
        queryset = get_producerskuprocurement_list(user, producer_uid, search_term)
        total_count = queryset.count()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serialier = ProducerSKUProcurementListSerializer(page, many=True)
            data = {"data": serialier.data, "total_count": total_count, "page_size": list_size}
            return self.get_paginated_response(data)
        serializer = ProducerSKUProcurementListSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

# Author Balu
class HubProducerImageListGetAPI(ExceptionHandlerMixin, APIView):
    """API to get Producer images"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubViewProducerPermission]

    def get(self, request):
        logged_user = request.user
        producer_uid = request.query_params.get("producer_uid")
        images = get_producer_images(logged_user, producer_uid)
        serializer = ProducerImageListSerializer(images,many=True)
        utility.log_save("API- HubProducerImageListGetAPI", "Get Producer images", logged_user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# Author Balu
class HubProducerVideoListGetAPI(ExceptionHandlerMixin, APIView):
    """API to get Producer videos"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubViewProducerPermission]

    def get(self, request):
        logged_user = request.user
        producer_uid = request.query_params.get("producer_uid")
        videos = get_producer_videos(logged_user, producer_uid)
        serializer = ProducerVideoListSerializer(videos,many=True)
        utility.log_save("API- HubProducerVideoListGetAPI", "Get Producer videos", logged_user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data=serializer.data)