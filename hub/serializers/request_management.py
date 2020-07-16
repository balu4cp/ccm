from rest_framework import serializers


class HubRequestsListSerializer(serializers.Serializer):
    """Serializer to get AdminFranchiseePrice List """

    id = serializers.IntegerField()
    uid = serializers.CharField()
    franchisee_name = serializers.SerializerMethodField()
    created_date = serializers.DateTimeField(format="%d %b %Y")
    product_name = serializers.CharField()
    quantity = serializers.IntegerField()
    delivery_date = serializers.DateField(format="%d %b %Y")
    status = serializers.SerializerMethodField()

    def get_franchisee_name(self, obj):
        return obj.franchisee.name

    def get_status(self, obj):
        return obj.get_status_display()


class HubRequestDetailsSerializer(serializers.Serializer):
    """Serializer to get Hubs List of Pricing Module"""

    id = serializers.IntegerField()
    uid = serializers.CharField()
    product_name = serializers.CharField()
    product_sku = serializers.CharField()
    quantity = serializers.IntegerField()
    created_date = serializers.DateTimeField(format="%d %b %Y")
    delivery_date = serializers.DateField(format="%d %b %Y")
    status = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    customer_uid = serializers.CharField()
    contact_number = serializers.CharField()
    email = serializers.CharField()
    delivery_location = serializers.CharField()
    delivery_franchisee = serializers.CharField()

    def get_status(self, obj):
        return obj.get_status_display()

    def get_customer_name(self, obj):
        return obj.customer.user.get_full_name()


class HubConvertToOrderDetailsSerializer(serializers.Serializer):
    """Serializer to get details for convert to order page"""

    delivery_franchisee = serializers.CharField()
    delivery_date = serializers.CharField()
    product_sku = serializers.CharField()
    product_name = serializers.CharField()
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    admin_controlled = serializers.BooleanField()
    delivery_charge = serializers.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    cgst = serializers.DecimalField(max_digits=10, decimal_places=2)
    sgst = serializers.DecimalField(max_digits=10, decimal_places=2)
    igst = serializers.DecimalField(max_digits=10, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    grand_total = serializers.DecimalField(max_digits=10, decimal_places=2)


class HubRequestStockStatusSerializer(serializers.Serializer):
    """ Serializer to get Request SKU Stock Status """

    stock_left = serializers.IntegerField()


class HubConvertToOrderSerializer(serializers.Serializer):
    """Serializer to Convert Request Item to Order """

    request_uid = serializers.CharField()
    grand_total = serializers.DecimalField(max_digits=10, decimal_places=2)


class HubMarkProcessedSerializer(serializers.Serializer):
    """Serializer to mark request item as processed """

    request_uid = serializers.CharField()
    status = serializers.CharField()
