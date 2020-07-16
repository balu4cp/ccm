from rest_framework.views import APIView  # Sreekanth
from rest_framework.response import Response  # Sreekanth
from rest_framework import status  # Sreekanth
from django.contrib.auth.models import User
from datetime import datetime, date
from common.mixins import (  # Sreekanth
    ExceptionHandlerMixin,
    CustomPagination,
    PaginationHandlerMixin
)
from ffadmin.serializers.stock_management import (
    OrganizationStockInfoListSerializer
)
from ffadmin.services.stock_management import (
    get_organization_stock_info_list
)
from common import utility
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from common.permissions import HubViewSKUPermission


# Author Jose
class HubOrganizationStockInfoListAPI(ExceptionHandlerMixin, APIView, PaginationHandlerMixin):
    # API for getting list of Stock Intends.
    pagination_class = CustomPagination
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubViewSKUPermission]

    def get(self, request):
        user = request.user
        list_size = request.query_params.get('list_size')
        if list_size in [None, '']:
            list_size = 10
        search_term = request.query_params.get('search_term')
        filter_date = request.query_params.get('date_filter')
        org_type = request.query_params.get('org_type')
        organization_id = request.query_params.get('organization_id')
        CustomPagination.page_size = list_size
        utility.log_save('API-FranchiseeOrganizationStockInfoListAPI', 'List fetched', user.username, 'GENERAL')
        queryset, dates_list = get_organization_stock_info_list(user, filter_date=filter_date, organization_id=organization_id, org_type=org_type, search_term=search_term)
        total_count = queryset.count()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = OrganizationStockInfoListSerializer(page, many=True)
            data = {
                'data': serializer.data,
                'total_count': total_count,
                'page_size': list_size,
                'dates': dates_list,
            }
            return self.get_paginated_response(data)
        serializer = OrganizationStockInfoListSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

