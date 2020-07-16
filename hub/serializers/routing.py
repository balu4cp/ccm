from rest_framework import serializers
from datetime import datetime
from django.conf import settings
from ffadmin.models import RoutingItem, HUB, Franchisee, ProcurementItem


class HubRoutingListSerializer(serializers.Serializer):
    """Serializer for Routing Items list"""

    id = serializers.IntegerField()
    uid = serializers.CharField()
    product = serializers.CharField()
    sku_uid = serializers.CharField()
    prior_location_name = serializers.CharField()
    next_location_name = serializers.CharField()
    package_date = serializers.DateField(format="%d/%m/%Y")
    organization_type = serializers.CharField()
    vehicle_number = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    shipping_uid = serializers.SerializerMethodField()
    processing_status = serializers.SerializerMethodField()
    shipping_status = serializers.SerializerMethodField()
    producer = serializers.SerializerMethodField()

    def get_vehicle_number(self, obj):
        return "" if obj.vehicle_number is None else obj.vehicle_number

    def get_organization(self, obj):
        if obj.organization_type == RoutingItem.HUB:
            return HUB.hubs.get(id=obj.organization_id).name
        else:
            return Franchisee.franchisees.get(id=obj.organization_id).name

    def get_shipping_uid(self, obj):
        return obj.shipping_uid if obj.shipping_uid is not None else ""

    def get_processing_status(self, obj):
        return obj.get_processing_status_display()

    def get_shipping_status(self, obj):
        return obj.get_shipping_status_display()

    def get_producer(self, obj):
        procurement = ProcurementItem.procurementitems.filter(id__in=obj.procurement_packages)
        return procurement[0].bulkitem.producer_id if procurement.exists() else ""


class HubGroupedRoutingListSerializer(serializers.Serializer):
    """Serializer for Routing Items list grouped by vehicle"""

    vehicle_id = serializers.CharField()
    data = serializers.ListField()


class HubUpdateVehicleSerializer(serializers.Serializer):
    """ Serializer for updating vehicle number in routing items list view"""

    vehicle_number = serializers.CharField()
    selected_ids = serializers.ListField(child=serializers.IntegerField())


class HubMergeRoutingItemsSerializer(serializers.Serializer):
    """ Serializer for merging routing items in list view"""

    selected_routings = serializers.ListField(child=serializers.IntegerField())


class HubUnifyShippingSerializer(serializers.Serializer):
    """ Serializer for unify shipping in routing items list view"""

    selected_routings = serializers.ListField(child=serializers.IntegerField())


class RoutingFiltersDataSerializer(serializers.Serializer):
    """ Serializer for unify shipping in routing items list view"""

    processing_status = serializers.ListField(child=serializers.CharField())
    shipping_status = serializers.ListField(child=serializers.CharField())
    prior_locations = serializers.ListField(child=serializers.CharField())
    next_locations = serializers.ListField(child=serializers.CharField())


class HubRoutingItemDetailProcurementListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    uid = serializers.CharField()
    franchisee_end = serializers.CharField()
    order_date = serializers.SerializerMethodField()
    order_uid = serializers.CharField()
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    next_location_name = serializers.CharField()

    def get_order_date(self, obj):
        return datetime.strftime(obj['order_date'], "%d/%m/%Y") if obj['order_date'] is not None else ""


class HubRoutingItemDetailsTransitHistorySerializer(serializers.Serializer):
    event_text = serializers.CharField()
    event_by = serializers.CharField()
    event_time = serializers.CharField()
    event_loc = serializers.CharField()


class HubRoutingItemDetailSerializer(serializers.Serializer):
    """Serializer for Routing Item Details"""

    producer = serializers.CharField()
    product = serializers.CharField()
    quantity = serializers.CharField(required=False)
    package_date = serializers.DateField(format="%d/%m/%Y")
    type = serializers.CharField()
    shipping_id = serializers.CharField(allow_null=True, allow_blank=True)
    shipping_qr = serializers.CharField(allow_null=True, allow_blank=True)
    shipping_status = serializers.CharField(allow_null=True, allow_blank=True)
    has_unified_shipping = serializers.BooleanField()
    delivery_date = serializers.DateField(format="%d/%m/%Y")
    vehicle_id = serializers.CharField()
    prior_loc = serializers.CharField()
    processing_status = serializers.CharField()
    transit_history = HubRoutingItemDetailsTransitHistorySerializer(many=True)
    procurements_list = HubRoutingItemDetailProcurementListSerializer(many=True)
    in_transit_once = serializers.BooleanField(default=False)
    is_next_routing = serializers.BooleanField(default=False)

    # def get_shipping_qr(self, obj):
    #     return f'{settings.MEDIA_URL}{obj["shipping_qr"]}' if obj['shipping_qr'] not in ['', None] else ""


class RoutingHUBFranchiseeListSerializer(serializers.Serializer):
    """Serializer for getting list of franchisee and hubs"""

    text = serializers.CharField()
    uid = serializers.CharField()


class HubRoutingGenerateNewItemSerializer(serializers.Serializer):
    """ Serializer for generating new item in detail page"""

    id = serializers.CharField()
    selected_procs = serializers.ListField(child=serializers.IntegerField())


class HubAutoUnmergeSerializer(serializers.Serializer):
    """ Serialzier for Routing Item Auto Unmerge"""

    uid = serializers.CharField()


class HubConfirmVehicleSerializer(serializers.Serializer):
    """ Serializer for confirming vehicle number for routing item"""

    uid = serializers.CharField()
    vehicle_id = serializers.CharField()


class HubRoutingMarkMissingSerializer(serializers.Serializer):
    """ Serializer for marking routing item as Missing"""

    uid = serializers.CharField()
    status = serializers.CharField()


class HubRoutingMarkDamagedSerializer(serializers.Serializer):
    """ Serializer for marking routing item as Damaged"""

    uid = serializers.CharField()
    status = serializers.CharField()


class HubRoutingGenerateShippingLabelSerializer(serializers.Serializer):
    """ Serializer for generating shipping label for routing item"""

    uid = serializers.CharField()


class HubRoutingUpdateItemSerializer(serializers.Serializer):
    """ Serializer for updating the details of routing item"""
    uid = serializers.CharField()
    vehicle_id = serializers.CharField()


class HubRoutingUpdateCurrentLocationSerializer(serializers.Serializer):
    """ Serializer for updating current location of routing item"""
    uid = serializers.CharField()
    selected_loc = serializers.CharField()
