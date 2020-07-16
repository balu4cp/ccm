from rest_framework.views import APIView  # Vishnupriya
from rest_framework.response import Response  # Vishnupriya
from rest_framework import status  # Vishnupriya
from django.contrib.auth.models import User
from common.mixins import (  # Vishnupriya
    ExceptionHandlerMixin,
    CustomPagination,
    PaginationHandlerMixin
)
from accounts.serializers.roles import (  # Vishnupriya
    PermissionListSerializer,
    RoleCreateSerializer,
    RoleListSerializer,
    RoleStatusChangeSerializer,
    RoleDetailsSerializer,
    RoleUpdateSerializer,
    RoleDeleteSerializer
)
from accounts.services.roles import (  # Vishnupriya
    get_permissions,
    role_create,
    get_roles,
    role_status_change,
    get_role_details,
    role_update,
    role_delete
)
from common import utility
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from common.permissions import HubViewRolePermission, HubCreateRolePermission, HubManageRolePermission


# Author Vishnupriya
class HubPermissionListView(ExceptionHandlerMixin, APIView):
    """API for getting list of Permissions."""
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated, HubViewRolePermission]
    
    def get(self, request):
        utility.log_save('HubPermissionListView', 'Get All Permissions', request.user.username, "GENERAL")
        role_type = "Hub"
        queryset = get_permissions(request.user, role_type)
        serializer = PermissionListSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
   

# Author Vishnupriya
class HubRoleCreateView(ExceptionHandlerMixin, APIView):
    """API for creating a single Role instance."""
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated, HubCreateRolePermission]

    def post(self, request):
        utility.log_save('HubRoleCreateView', 'Role Created', request.user.username, "GENERAL")
        serializer = RoleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role_create(**serializer.validated_data, user=request.user)
        return Response(status=status.HTTP_201_CREATED, data="Role created successfully")


# Author Vishnupriya
class HubRoleListView(ExceptionHandlerMixin, APIView, PaginationHandlerMixin):
    """API for getting list of Roles."""
    pagination_class = CustomPagination
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated, HubViewRolePermission]
    
    def get(self, request):
        utility.log_save('HubRoleListView', 'Role List Get', request.user.username, "GENERAL")
        role_type = "Hub"
        search_term = request.query_params.get('search_term')
        list_size = request.query_params.get('list_size')
        CustomPagination.page_size = list_size
        queryset = get_roles(request.user, role_type, search_term)
        total_count = queryset.count()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RoleListSerializer(page, many=True)
            data = {
                'data': serializer.data,
                'total_count': total_count,
                'page_size': list_size,
            }
            return self.get_paginated_response(data)

        serializer = RoleListSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# Author Vishnupriya
class HubRoleStatusChangeView(ExceptionHandlerMixin, APIView):
    """API for changing the status of Role. (Activate/ Deactivate)"""
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated, HubManageRolePermission]
    
    def post(self, request):
        utility.log_save('HubRoleStatusChangeView', 'Role Status Changed', request.user.username, "GENERAL")
        serializer = RoleStatusChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = role_status_change(**serializer.validated_data, user=request.user)
        return Response(status=status.HTTP_200_OK, data=data)


# Author Vishnupriya
class HubRoleDetailedView(ExceptionHandlerMixin, APIView):
    """API for getting details of a signle Role Instance"""
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated, HubViewRolePermission]
    
    def get(self, request):
        utility.log_save('HubRoleDetailedView', 'Role Details Get', request.user.username, "GENERAL")
        role_id = request.query_params.get('role_id')
        queryset = get_role_details(request.user, role_id)
        serializer = RoleDetailsSerializer(queryset)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# Author Vishnupriya
class HubRoleUpdateView(ExceptionHandlerMixin, APIView):
    """API for updating a single Role instance."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubManageRolePermission]
    
    def post(self, request):
        utility.log_save('HubRoleUpdateView', 'Role Updated', request.user.username, "GENERAL")
        serializer = RoleUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role_update(**serializer.validated_data, user=request.user)
        return Response(status=status.HTTP_200_OK, data="Role updated successfully")


# Author Vishnupriya
class HubRoleDeleteView(ExceptionHandlerMixin, APIView):
    """API for Deleting Role Details View."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubManageRolePermission]

    def post(self, request):
        utility.log_save('HubRoleDeleteView', 'Role Deleted', request.user.username, "GENERAL")
        serializer = RoleDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role_delete(**serializer.validated_data, user=request.user)
        return Response(status=status.HTTP_200_OK, data="Role Deleted Successfully")


        