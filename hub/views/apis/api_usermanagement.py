from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
from common.mixins import ExceptionHandlerMixin 
from django.http import HttpResponseRedirect
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from accounts.serializers.usermanagement import UserCreateSerializer,AdminUsersListSerializer,AdminUserPasswordResetSerializer,AdminUserResenEmailSerializer,AdminUserStatusChangeSerializer,AdminUsersDetailSerializer,AdminUserUpdateSerializer
from accounts.services.usermanagement import user_create,get_users_list,reset_password,resend_activation_email,user_status_change,get_user_details,update_user_details
from common.mixins import (
    ExceptionHandlerMixin,
    PaginationHandlerMixin,
    CustomPagination,
)

from common.permissions import HubViewUserPermission, HubCreateUserPermission, HubManageUserPermission
from common import utility


class HubUserCreateAPI(ExceptionHandlerMixin, APIView):
    """API for creating new User ."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,HubCreateUserPermission]
    
    def post(self, request):
        user = request.user
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_create(user=user,type='Hub',**serializer.validated_data)
        utility.log_save('HubUserCreateAPI','Hub-user created', user.username, 'GENERAL')
        return Response(status=status.HTTP_200_OK, data="User Created successfully.")



class HubUserListAPI(ExceptionHandlerMixin, APIView, PaginationHandlerMixin):
    """API for getting User list View."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,HubViewUserPermission]

    pagination_class = CustomPagination
    
    def get(self, request):
        user = request.user
        search_term = request.query_params.get("search_term")
        list_size = request.query_params.get("list_size")
        CustomPagination.page_size = list_size
        users = get_users_list(search_term,list_size,user)
        total_count = users.count()
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = AdminUsersListSerializer(page, many=True)
            data = {
                "data": serializer.data,
                "total_count": total_count,
                'page_size': list_size,
            }
            utility.log_save('HubUserListAPI','Hub-user list fetched', user.username, 'GENERAL')
            return self.get_paginated_response(data)
        serializer = AdminUsersListSerializer(users,many=True)
        utility.log_save('HubUserListAPI','Hub-user list fetched', user.username, 'GENERAL')
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class HubUserDetailsAPI(ExceptionHandlerMixin, APIView):
    """API for Getting user Details View."""
    authentication_classes = [SessionAuthentication,HubViewUserPermission]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_id = request.query_params.get("user_id")
        beacon_details = get_user_details(user,user_id)
        serializer = AdminUsersDetailSerializer(beacon_details)
        utility.log_save('HubUserDetailsAPI','Hub-user details fetched', user.username, 'GENERAL')
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class HubUserResetPasswordAPI(ExceptionHandlerMixin, APIView):
    """API for reset a new passwod ."""
    authentication_classes = [SessionAuthentication,HubManageUserPermission]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        serializer = AdminUserPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        msg=reset_password(logged_user=user,**serializer.validated_data)
        utility.log_save('HubUserResetPasswordAPI','Hub-user password changed', user.username, 'GENERAL')
        return Response(status=status.HTTP_200_OK, data=msg)


class HubUserResendEmailAPI(ExceptionHandlerMixin, APIView):
    """API for rsend account activation mail ."""
    authentication_classes = [SessionAuthentication,HubManageUserPermission]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        serializer = AdminUserResenEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resend_activation_email(logged_user=user,**serializer.validated_data)
        utility.log_save('HubUserResendEmailAPI','Hub-user email sent', user.username, 'GENERAL')
        return Response(status=status.HTTP_200_OK, data='Email sent successfully.')

class HubUserStatusChangeAPI(ExceptionHandlerMixin, APIView):
    """API for enable or disable account ."""
    authentication_classes = [SessionAuthentication,HubManageUserPermission]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        serializer = AdminUserStatusChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_status_change(user=user, **serializer.validated_data)
        utility.log_save('HubUserStatusChangeAPI','Hub-user status changed', user.username, 'GENERAL')
        return Response(status=status.HTTP_200_OK, data='Status changed.')



class HubUserUpdateAPI(ExceptionHandlerMixin, APIView):
    """API for updating  User ."""
    authentication_classes = [SessionAuthentication,HubManageUserPermission]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        serializer = AdminUserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_user_details(user=user, **serializer.validated_data)
        utility.log_save('HubUserUpdateAPI','Hub-user updated', user.username, 'GENERAL')
        return Response(status=status.HTTP_200_OK, data="User updated successfully.")