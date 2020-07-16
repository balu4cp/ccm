from rest_framework import serializers


class HubsGetSerializer(serializers.Serializer):
    """Serializer to get Hub basic detail for Create  franchisee"""

    id = serializers.IntegerField()
    name = serializers.CharField()
    state = serializers.CharField()
    district = serializers.CharField()
    regions = serializers.ListField()

class StatesGetSerializer(serializers.Serializer):
    """Serializer to get state List for Create  franchisee"""

    state_name = serializers.CharField()


class DistrictsGetSerializer(serializers.Serializer):
    """Serializer to get district List for Create  franchisee"""

    district = serializers.CharField()

class PincodesSerializer(serializers.Serializer):
    """Serializer to get pincode List for Create  franchisee"""

    pincode = serializers.CharField()


class FranchiseeCreateSerializer(serializers.Serializer):
    """Serializer to  Create  franchisee"""

    franchisee_name = serializers.CharField()
    type = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField()
    selected_hub = serializers.IntegerField()
    sales_commision = serializers.DecimalField(max_digits=5, decimal_places=2,required=False)
    procurement_commision = serializers.DecimalField(max_digits=5, decimal_places=2,required=False)
    admin_name = serializers.CharField()
    admin_contact_no = serializers.CharField()
    alt_contact_no = serializers.CharField(required=False, allow_blank=True)
    admin_email = serializers.CharField()
    radius = serializers.DecimalField(max_digits=6, decimal_places=2,required=False)
    latitude = serializers.CharField(required=False, allow_blank=True)
    longitude = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    gstin = serializers.CharField()
    selected_region = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    selected_state = serializers.CharField()
    selected_district = serializers.CharField()
    selected_pincode = serializers.ListField()


class AddFranchiseeContactSerializer(serializers.Serializer):
    """Serializer to  Create  franchisee  contact"""

    franchisee_id = serializers.IntegerField()
    contact_name = serializers.CharField()
    contact_designation = serializers.CharField()
    contact_phone = serializers.CharField()
    contact_email = serializers.CharField()
    contact_alt_no = serializers.CharField(required=False, allow_blank=True)


class FranchiseeContactListSerializer(serializers.Serializer):
    """Serializer to get contact List for   franchisee"""

    id = serializers.IntegerField()
    name = serializers.CharField()
    designation = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.CharField()
    alternate_phone = serializers.CharField(required=False, allow_blank=True)

class UpdateFranchiseeContactSerializer(serializers.Serializer):
    """Serializer to update contact of  franchisee"""

    contact_id = serializers.IntegerField()
    contact_name = serializers.CharField()
    contact_designation = serializers.CharField()
    contact_phone = serializers.CharField()
    contact_email = serializers.CharField()
    contact_alt_no = serializers.CharField(required=False, allow_blank=True)


class FranchiseerStatusChangeSerializer(serializers.Serializer):
    """Serializer to Update franchisee Status"""

    franchisee_id = serializers.IntegerField()
    status = serializers.BooleanField()


class FranchiseeResenEmailSerializer(serializers.Serializer):
    """Serializer to resend email"""
    
    franchisee_id = serializers.IntegerField(required=True)


class FranchiseeDetailSerializer(serializers.Serializer):
    """Serializer to get details of   franchisee"""

    id = serializers.CharField()
    name = serializers.CharField()
    type = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField()
    hub__id = serializers.IntegerField()
    sales_commission = serializers.DecimalField(max_digits=5, decimal_places=2,required=False)
    procurement_commission = serializers.DecimalField(max_digits=5, decimal_places=2,required=False)
    admin_name = serializers.CharField()
    admin_phone = serializers.CharField()
    alternate_phone = serializers.CharField(required=False, allow_blank=True)
    admin_email = serializers.CharField()
    service_radius = serializers.DecimalField(max_digits=6, decimal_places=2,required=False)
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    address = serializers.CharField(required=False, allow_blank=True)
    gstin_number = serializers.CharField()
    region = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField()
    district = serializers.CharField()
    service_pincodes = serializers.ListField()
    is_disabled = serializers.BooleanField()
    is_used = serializers.BooleanField()

    def get_latitude(self, obj):
        if obj['location'] not in [None]:
            return obj['location'].x
        else:
            return ''
    def get_longitude(self, obj):
        if obj['location'] not in [None]:
            return obj['location'].y
        else:
            return ''


class FranchiseeUpdateSerializer(serializers.Serializer):
    """Serializer to update  franchisee"""

    franchisee_id = serializers.IntegerField()
    franchisee_name = serializers.CharField()
    type = serializers.CharField(required=False, allow_blank=True)
    selected_hub = serializers.IntegerField()
    sales_commision = serializers.DecimalField(max_digits=5, decimal_places=2,required=False)
    procurement_commision = serializers.DecimalField(max_digits=5, decimal_places=2,required=False)
    admin_name = serializers.CharField()
    admin_contact_no = serializers.CharField()
    alt_contact_no = serializers.CharField(required=False, allow_blank=True)
    admin_email = serializers.CharField()
    radius = serializers.DecimalField(max_digits=6, decimal_places=2,required=False)
    latitude = serializers.CharField(required=False, allow_blank=True)
    longitude = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    gstin = serializers.CharField()
    selected_region = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    selected_state = serializers.CharField()
    selected_district = serializers.CharField()
    selected_pincode = serializers.ListField()


class HubFranchiseeListSerializer(serializers.Serializer):
    """Serializer to get franchisee List of a HUB"""

    id = serializers.IntegerField()
    name = serializers.CharField()
    state = serializers.CharField()
    admin_name = serializers.CharField()
    admin_phone = serializers.CharField()
    district = serializers.CharField()
    uid = serializers.CharField()
    region = serializers.CharField(required=False, allow_blank=True)