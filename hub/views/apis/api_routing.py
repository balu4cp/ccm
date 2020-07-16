import json
from rest_framework.views import APIView  # Jose
from rest_framework.response import Response  # Jose
from rest_framework import status  # Jose
from common.mixins import ExceptionHandlerMixin
from hub.serializers.routing import (  # Jose
    HubRoutingListSerializer,
    HubGroupedRoutingListSerializer,
    HubRoutingItemDetailSerializer,
    HubAutoUnmergeSerializer,
    HubUpdateVehicleSerializer,
    HubConfirmVehicleSerializer,
    HubMergeRoutingItemsSerializer,
    HubUnifyShippingSerializer,
    RoutingFiltersDataSerializer,
    HubRoutingMarkMissingSerializer,
    HubRoutingMarkDamagedSerializer,
    HubRoutingGenerateShippingLabelSerializer,
    HubRoutingUpdateItemSerializer,
    HubRoutingGenerateNewItemSerializer,
    RoutingHUBFranchiseeListSerializer,
    HubRoutingUpdateCurrentLocationSerializer,
)
from ffadmin.services.routing import (  # Jose
    get_routing_list,
    get_grouped_routing_list,
    get_routing_item_details,
    auto_unmerge_routing,
    update_vehicle,
    confirm_vehicle,
    merge_routing_items,
    unify_shipping,
    get_routing_filters_list,
    mark_shipping_status,
    update_item,
    generate_new_item,
    generate_shipping_label,
    get_hub_franchisee_list,
    update_item_location,
)
from common import utility
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from common.permissions import (
    HubViewRoutingListPermission,
    HubRoutingMarkMissingDamagedPermission,
    HubRoutingChangeLocationPermission,
    HubManageRoutingPermission,
)


# Author Jose
class HubRoutingListView(ExceptionHandlerMixin, APIView):
    """API for Getting Hub Routing List View."""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubViewRoutingListPermission]

    def get(self, request):
        user = request.user
        date_filter = request.query_params.get('dateFilter')
        list_queryset, filters_dict = get_routing_list(user, date_filter)
        list_serializer = HubRoutingListSerializer(list_queryset, many=True)
        group_queryset = get_grouped_routing_list(user, list_serializer.data)
        group_serializer = HubGroupedRoutingListSerializer(group_queryset, many=True)
        filters_dict = RoutingFiltersDataSerializer(filters_dict)
        data = {
            "routing_list": list_serializer.data,
            "grouped_list": group_serializer.data,
            "filters_dict": filters_dict.data
        }
        utility.log_save("API- RoutingListView", "Routing List get", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data=data)


# Author Jose
class HubUpdateVehicle(ExceptionHandlerMixin, APIView):
    """ API for Updating Vehicles of Routing Item."""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubManageRoutingPermission]

    def post(self, request):
        data = {
            "vehicle_number": request.data["vehicle_number"],
            "selected_ids": json.loads(request.data["selected_ids"]),
        }
        user = request.user
        serializer = HubUpdateVehicleSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        update_vehicle(user, **serializer.validated_data)
        utility.log_save("API- HubUpdateVehicle", "Vehicle updated successfully", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data="Vehicle updated successfully")


class HubMergeRoutingItems(ExceptionHandlerMixin, APIView):
    """ API to Merge Routing Items in list view. """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubManageRoutingPermission]

    def post(self, request):
        user = request.user
        data = {"selected_routings": json.loads(request.data["selected_routings"])}
        serializer = HubMergeRoutingItemsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        merge_routing_items(user, **serializer.validated_data)
        utility.log_save("API-HubMergeRoutingItems", "Merged successfully", user.username, "GENERAL")
        return Response(status=status.HTTP_201_CREATED, data="Items merged successfully")


class HubUnifyShipping(ExceptionHandlerMixin, APIView):
    """ API to Unify Shipping in Routing List View. """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubManageRoutingPermission]

    def post(self, request):
        user = request.user
        data = {"selected_routings": json.loads(request.data["selected_routings"])}
        serializer = HubUnifyShippingSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        unify_shipping(user, **serializer.validated_data)
        utility.log_save("API- HubUnifyShipping", "Items shipping unified successfully", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data="Items shipping unified")


# Author Jose
class RoutingListFiltersGet(ExceptionHandlerMixin, APIView):
    """ API to get list of filter lists for Routing List View. """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        date_filter = request.query_params.get('date_filter')
        queryset = get_routing_filters_list(user, date_filter)
        serializer = RoutingFiltersDataSerializer(queryset)
        utility.log_save("API- RoutingListFiltersGet", "Filters List Get", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# Author Jose
class HubRoutingItemDetailsView(ExceptionHandlerMixin, APIView):
    """ API for getting HUB/Franchisee Routing Item Details View."""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubViewRoutingListPermission]

    def get(self, request):
        user = request.user
        routing_id = request.query_params.get("uid")
        queryset = get_routing_item_details(user, routing_id)
        serializer = HubRoutingItemDetailSerializer(queryset)
        utility.log_save("API- HubRoutingItemDetailsView", "Routing Item Details get", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# Author Jose
class RoutingHUBFranchiseeListGet(ExceptionHandlerMixin, APIView):
    """ API to get list of HUBs and franchisees for Routing Detail View """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        queryset = get_hub_franchisee_list(user)
        serializer = RoutingHUBFranchiseeListSerializer(queryset, many=True)
        utility.log_save("API- RoutingListFiltersGet", "Filters List Get", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# Author Jose
class HubAutoUnmergeItem(ExceptionHandlerMixin, APIView):
    """ API for Auto Unmerge Routing Item."""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubManageRoutingPermission]

    def post(self, request):
        user = request.user
        serializer = HubAutoUnmergeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auto_unmerge_routing(user, **serializer.validated_data)
        utility.log_save("API- HubAutoUnmergeItem", "Routing Item unmerged", user.username, "GENERAL")
        return Response(status=status.HTTP_201_CREATED, data="Unmerged successfully")


# Author Jose
class HubConfirmVehicle(ExceptionHandlerMixin, APIView):
    """ API for Confirm Vehicle of Routing Item."""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubManageRoutingPermission]

    def post(self, request):
        user = request.user
        serializer = HubConfirmVehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirm_vehicle(user, **serializer.validated_data)
        utility.log_save("API- HubConfirmVehicle", "Vehicle updated successfully", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data="Vehicle confirmed")


# Author Jose
class HubRoutingMarkDamaged(ExceptionHandlerMixin, APIView):
    """ API for Marking Routing Item as Damaged"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubRoutingMarkMissingDamagedPermission]

    def post(self, request):
        user = request.user
        serializer = HubRoutingMarkDamagedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mark_shipping_status(user, **serializer.validated_data)
        utility.log_save("API- HubRoutingMarkDamaged", "Item marked as Damaged", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data="Item marked as Damaged")


# Author Jose
class HubRoutingMarkMissing(ExceptionHandlerMixin, APIView):
    """ API for Marking Routing Item as Missing"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubRoutingMarkMissingDamagedPermission]

    def post(self, request):
        user = request.user
        serializer = HubRoutingMarkMissingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mark_shipping_status(user, **serializer.validated_data)
        utility.log_save("API- HubRoutingMarkMissing", "Item marked as Missing", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data="Item marked as Missing")


# Author Jose
class HubRoutingGenerateShippingLabel(ExceptionHandlerMixin, APIView):
    """ API for Generating Shipping Label for Routing Item"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubManageRoutingPermission]

    def post(self, request):
        user = request.user
        serializer = HubRoutingGenerateShippingLabelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        generate_shipping_label(user, **serializer.validated_data)
        utility.log_save("API- HubRoutingGenerateShippingLabel", "Shipping label generated", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data="Shipping label generated")


# Author Jose
class HubRoutingUpdateItem(ExceptionHandlerMixin, APIView):
    """ API for Marking Routing Item as Missing"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubManageRoutingPermission]

    def post(self, request):
        user = request.user
        serializer = HubRoutingUpdateItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_item(user, **serializer.validated_data)
        utility.log_save("API- HubRoutingUpdateItem", "Item updated successfully", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data="Item updated successfully")


# Author Jose
class HubRoutingGenerateNewItem(ExceptionHandlerMixin, APIView):
    """ API for Marking Routing Item as Missing"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubManageRoutingPermission]

    def post(self, request):
        user = request.user
        data2 = {"uid": request.data["uid"], "selected_procs": json.loads(request.data["selected_ids"])}
        serializer = HubRoutingGenerateNewItemSerializer(data=data2)
        serializer.is_valid(raise_exception=True)
        generate_new_item(user, **serializer.validated_data)
        utility.log_save("API- HubRoutingGenerateNewItem", "New item generated", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data="New item generated")


# Author Jose
class HubRoutingUpdateCurrentLocation(ExceptionHandlerMixin, APIView):
    """ API for updating the current location of RoutingItem"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, HubRoutingChangeLocationPermission]

    def post(self, request):
        user = request.user
        serializer = HubRoutingUpdateCurrentLocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_item_location(user, **serializer.validated_data)
        utility.log_save("API- HubRoutingUpdateCurrentLocation", "Current Location updated", user.username, "GENERAL")
        return Response(status=status.HTTP_200_OK, data="Current location updated")
