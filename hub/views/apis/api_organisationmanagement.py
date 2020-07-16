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
from hub.serializers.franchisee import (
    HubsGetSerializer, FranchiseeCreateSerializer, HubFranchiseeListSerializer,
    FranchiseeUpdateSerializer, FranchiseeContactListSerializer, AddFranchiseeContactSerializer,
    FranchiseeUpdateSerializer, UpdateFranchiseeContactSerializer, FranchiseerStatusChangeSerializer,
    FranchiseeResenEmailSerializer, FranchiseeDetailSerializer,
    )
from common.permissions import (
    HubViewOrganisationPermission, HubCreateOrganisationPermission, HubManageOrganisationPermission
    )
from hub.services.organisationmanagement import (
    get_hub_details, get_hub_francisees_list
    )
from ffadmin.services.franchisee import (
    create_franchisee, add_franchisee_contact, get_franchisee_contacts,
    update_franchisee_contact, franchisee_status_change, get_franchisee_details,
    resend_activation_email, update_franchisee_object,
    )
from common import utility

class HubBasicInfoGetAPI(ExceptionHandlerMixin, APIView):
    """API for getting hub details of user ."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        utility.log_save('HubBasicInfoGetAPI', 'Hub Basic Info Get', request.user.username, "GENERAL")
        user = request.user
        data=get_hub_details(user)
        serializer = HubsGetSerializer(data)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class HubFranchiseeCreateAPI(ExceptionHandlerMixin, APIView):
    """API for creating new franchisee ."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,HubCreateOrganisationPermission]
    
    def post(self, request):
        utility.log_save('HubFranchiseeCreateAPI', 'Franchisee Created', request.user.username, "GENERAL")
        user = request.user
        serializer = FranchiseeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_franchisee(logged_user=user, **serializer.validated_data)
        return Response(status=status.HTTP_200_OK, data="Franchisee Created successfully.")


class HubFranchiseeListAPI(ExceptionHandlerMixin, APIView, PaginationHandlerMixin):
    """API for getting Franchisee list View."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,HubViewOrganisationPermission]

    pagination_class = CustomPagination
    
    def get(self, request):
        utility.log_save('HubFranchiseeListAPI', 'Franchisee List Get', request.user.username, "GENERAL")
        user = request.user
        search_term = request.query_params.get("search_term")
        list_size = request.query_params.get("list_size")
        CustomPagination.page_size = list_size
        franchisees = get_hub_francisees_list(list_size,user,search_term)
        total_count = franchisees.count()
        page = self.paginate_queryset(franchisees)
        if page is not None:
            serializer = HubFranchiseeListSerializer(page, many=True)
            data = {
                "data": serializer.data,
                "total_count": total_count,
                'page_size': list_size,
            }
            return self.get_paginated_response(data)
        serializer = HubFranchiseeListSerializer(franchisees,many=True)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class HubFranchiseeDetailsAPI(ExceptionHandlerMixin, APIView):
    """API for Getting franchisee Details View."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,HubViewOrganisationPermission]

    def get(self, request):
        utility.log_save('HubFranchiseeDetailsAPI', 'Franchisee Details Get', request.user.username, "GENERAL")
        user = request.user
        franchisee_id = request.query_params.get("franchisee_id")
        details = get_franchisee_details(user, franchisee_id)
        serializer = FranchiseeDetailSerializer(details)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class HubFranchiseeUpdateAPI(ExceptionHandlerMixin, APIView):
    """API for update franchisee details ."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,HubManageOrganisationPermission]
    
    def post(self, request):
        utility.log_save('HubFranchiseeUpdateAPI', 'Franchisee Updated', request.user.username, "GENERAL")
        user = request.user
        serializer = FranchiseeUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_franchisee_object(logged_user=user, **serializer.validated_data)
        return Response(status=status.HTTP_200_OK, data="Franchisee updated successfully.")


class HubFracchiseeContactListAPI(ExceptionHandlerMixin, APIView):
    """API for getting franchisee  contacts."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,HubViewOrganisationPermission]
    
    def get(self, request):
        utility.log_save('HubFracchiseeContactListAPI', 'Franchisee Contact List Get', request.user.username, "GENERAL")
        user = request.user
        franchisee_id = request.query_params.get("franchisee_id")
        contacts = get_franchisee_contacts(user, franchisee_id)
        serializer = FranchiseeContactListSerializer(contacts, many=True)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class HubFracchiseeContactCreateAPI(ExceptionHandlerMixin, APIView):
    """API for creating  franchisee contacts ."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,HubManageOrganisationPermission]
    
    def post(self, request):
        utility.log_save('HubFracchiseeContactCreateAPI', 'Franchisee Contact Created', request.user.username, "GENERAL")
        user = request.user
        serializer = AddFranchiseeContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        add_franchisee_contact(logged_user=user, **serializer.validated_data)
        return Response(status=status.HTTP_200_OK, data="Contact added successfully.")


class HubFracchiseeContactUpdateAPI(ExceptionHandlerMixin, APIView):
    """API for updating contacts ."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,HubManageOrganisationPermission]

    def post(self, request):
        utility.log_save('HubFracchiseeContactUpdateAPI', 'Franchisee Contact Updated', request.user.username, "GENERAL")
        user = request.user
        serializer = UpdateFranchiseeContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_franchisee_contact(logged_user=user, **serializer.validated_data)
        return Response(status=status.HTTP_200_OK, data="Contact updated successfully.")


class HubFranchiseeStatusChangeAPI(ExceptionHandlerMixin, APIView):
    """API for enable or disable  franchisee account ."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,HubManageOrganisationPermission]
    def post(self, request):
        utility.log_save('HubFranchiseeStatusChangeAPI', 'Franchisee Status changed', request.user.username, "GENERAL")
        user = request.user
        serializer = FranchiseerStatusChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        franchisee_status_change(logged_user=user, **serializer.validated_data)
        return Response(status=status.HTTP_200_OK, data='Status changed.')


class HubFranchiseerResendEmailAPI(ExceptionHandlerMixin, APIView):
    """API for rsend account activation mail ."""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,HubManageOrganisationPermission]
    
    def post(self, request):
        utility.log_save('HubFranchiseerResendEmailAPI', 'Franchisee Resent Email', request.user.username, "GENERAL")
        user = request.user
        serializer = FranchiseeResenEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resend_activation_email(**serializer.validated_data, user=user)
        return Response(status=status.HTTP_200_OK, data='Email sent successfully.')