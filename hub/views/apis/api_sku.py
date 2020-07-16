from rest_framework.views import APIView  # Sreekanth
from rest_framework.response import Response  # Sreekanth
from rest_framework import status  # Sreekanth
from django.contrib.auth.models import User
from common.mixins import ( 
    ExceptionHandlerMixin,
    CustomPagination,
    PaginationHandlerMixin
)
from hub.serializers.sku import ( 
    HubSKUListSerializer,
    HubSKUDetailSerializer,
    SKUCreateSerializer,
    SKUUpdateSerializer,
    SKUStatusChangeSerializer
)
from ffadmin.services.sku import ( 
    get_sku_list,
    get_sku_details,
    sku_create,
    sku_update,
    sku_status_change
)
from common import utility
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from common.permissions import HubViewSKUPermission,HubCreateSKUPermission,HubManageSKUPermission


# Author Sreekanth
class HubSKUListView(ExceptionHandlerMixin, APIView, PaginationHandlerMixin):
    """API for getting list of SKUs."""
    pagination_class = CustomPagination
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,HubViewSKUPermission]
    
    def get(self, request):
        user = request.user
        list_size = request.query_params.get('list_size')
        if list_size in [None,'']:
            list_size = 10
        search_term = request.query_params.get('search_term')
        CustomPagination.page_size = list_size
        utility.log_save('API- Hub SKU List Get','Get list of SKUs', user.username, 'GENERAL')
        queryset = get_sku_list(user, list_size,search_term)
        total_count = queryset.count()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = HubSKUListSerializer(page, many=True)
            data = {
                'data': serializer.data,
                'total_count': total_count,
                'page_size': list_size,
            }
            return self.get_paginated_response(data)
        serializer = HubSKUListSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# Author Sreekanth
class HubSkuDetailGetAPI(ExceptionHandlerMixin, APIView):
    """API for Getting SKU Details View."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,HubViewSKUPermission]

    def get(self, request):
        user = request.user
        sku_uid = request.query_params.get("sku_uid")
        details = get_sku_details(user,sku_uid)
        serializer = HubSKUDetailSerializer(details)
        utility.log_save('API- Hub SKU Details View Get','SKU Details fetch', user.username, 'GENERAL')
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


#BALU
class HubSkuCreateAPI(ExceptionHandlerMixin, APIView):
    """API for creating a single SKU instance."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,HubCreateSKUPermission]

    def post(self, request):
        user = request.user
        serializer = SKUCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sku_create(**serializer.validated_data, user=request.user)
        utility.log_save('API- Hub SKU  Create','SKU created successfully by '+user.username, user.username, 'GENERAL')
        return Response(status=status.HTTP_201_CREATED, data="SKU created successfully")

#BALU
class HubSkuUpdateAPI(ExceptionHandlerMixin, APIView):
    """API for updating a single SKU instance."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,HubManageSKUPermission]

    def post(self, request):
        user = request.user
        serializer = SKUUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sku_update(**serializer.validated_data, user=request.user)
        utility.log_save('API- Hub SKU  Updated','Sku updated successfully by '+user.username, user.username, 'GENERAL')
        return Response(status=status.HTTP_201_CREATED, data="SKU updated successfully")

#BALU
class HubSKUStatusChangeView(ExceptionHandlerMixin, APIView):
    """API for enable or disable account ."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,HubManageSKUPermission]
    
    def post(self, request):
        user = request.user
        serializer = SKUStatusChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sku_status_change(logged_user=user, **serializer.validated_data)
        utility.log_save('API- Hub SKU  Status Toggle','SKU Status Changed by '+user.username, user.username, 'GENERAL')
        return Response(status=status.HTTP_200_OK, data='Status changed.')