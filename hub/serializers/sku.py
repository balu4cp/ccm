import os
from django.conf import settings
from rest_framework import serializers

class HubSKUListSerializer(serializers.Serializer):
    """Serializer to get sku List """
    id = serializers.IntegerField()
    uid = serializers.CharField()
    name = serializers.CharField()
    category__name = serializers.CharField()
    sub_category__name = serializers.CharField()
    expiry_period = serializers.IntegerField()
    no_of_producer = serializers.IntegerField()
    is_disabled = serializers.BooleanField()


class SubCategoryGetSerializer(serializers.Serializer):
    """Serializer to get sku sub categories List for Create  sku"""

    id = serializers.IntegerField()
    name = serializers.CharField()

    
class SKUPriceComponentSerializer(serializers.Serializer):
    """Serializer to get SKUPriceComponent Detail"""
    id = serializers.IntegerField()
    component_name = serializers.CharField()
    percentage = serializers.DecimalField(max_digits=6, decimal_places=2)


class SKUImageSerializer(serializers.Serializer):
    """Serializer to get SKU Image Detail"""
    id = serializers.IntegerField()
    image = serializers.SerializerMethodField()

    def get_image(self,obj):
        media_url = settings.MEDIA_URL
        if obj.image:
            image = media_url+str(obj.image.path)
        return image


class HubSKUDetailSerializer(serializers.Serializer):
    """Serializer to get SKU Detail"""
    name = serializers.CharField()
    uom_id = serializers.IntegerField()
    minimum_uom = serializers.DecimalField(max_digits=10, decimal_places=2)
    uom_increment = serializers.DecimalField(max_digits=10, decimal_places=2)
    category_id = serializers.IntegerField()
    sub_category_id = serializers.IntegerField()
    expiry_period = serializers.IntegerField()
    type = serializers.CharField()
    alternate_names = serializers.CharField(required=False, allow_blank=True)
    search_parameters = serializers.CharField(required=False, allow_blank=True)
    default_cost_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    offer_price = serializers.DecimalField(max_digits=10, decimal_places=2,required=False, allow_null=True)
    default_selling_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_product_seasonal = serializers.BooleanField()
    is_disabled = serializers.BooleanField()
    description = serializers.CharField(required=False, allow_blank=True)
    alternative_names_list = serializers.SerializerMethodField()
    search_parameters_list = serializers.SerializerMethodField()
    skupricecomponents = SKUPriceComponentSerializer(many=True,required=False)
    skuimages = SKUImageSerializer(many=True,required=False)
    skucategorys = SubCategoryGetSerializer(many=True)
    is_admin_controlled = serializers.BooleanField()
    product_margin = serializers.DecimalField(max_digits=10, decimal_places=2,required=False, allow_null=True)
    delivery_charge = serializers.DecimalField(max_digits=10, decimal_places=2,required=False, allow_null=True)


    def get_alternative_names_list(self,obj):
        if obj['alternate_names'] not in [None,'',[]]:
            return obj['alternate_names'][0].split(',')
        else:
            return []


    def get_search_parameters_list(self,obj):
        if obj['search_parameters'] not in [None,'',[]]:
            return obj['search_parameters'][0].split(',')
        else:
            return []


class SKUCreateSerializer(serializers.Serializer):
    """Serializer to Create  sku"""
    product_name = serializers.CharField()
    uom = serializers.IntegerField()
    minimum_uom = serializers.DecimalField(max_digits=10, decimal_places=3)
    uom_increment = serializers.DecimalField(max_digits=10, decimal_places=3)
    category_id = serializers.IntegerField()
    subcategory_id = serializers.IntegerField()
    expiry_period = serializers.IntegerField()
    type = serializers.CharField()
    alternative_names = serializers.ListField(allow_empty=True)
    search_parameters = serializers.ListField(allow_empty=True)
    default_cost_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    offer_price = serializers.DecimalField(max_digits=10, decimal_places=2,required=False, allow_null=True)
    default_selling_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    cgst_percentage = serializers.DecimalField(max_digits=6, decimal_places=2,required=False, allow_null=True)
    sgst_percentage = serializers.DecimalField(max_digits=6, decimal_places=2,required=False, allow_null=True)
    igst_percentage = serializers.DecimalField(max_digits=6, decimal_places=2,required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True)
    seasonal_product = serializers.BooleanField()
    product_images = serializers.ListField(child=serializers.FileField(), allow_empty=True, min_length=None, max_length=None)
    is_admin_controlled = serializers.BooleanField()
    margin = serializers.DecimalField(max_digits=10, decimal_places=2,required=False, allow_null=True)
    delivery_charge = serializers.DecimalField(max_digits=10, decimal_places=2,required=False, allow_null=True)


class SKUUpdateSerializer(serializers.Serializer):
    """Serializer to update  sku"""
    sku_uid = serializers.CharField()
    product_name = serializers.CharField()
    uom = serializers.IntegerField()
    minimum_uom = serializers.DecimalField(max_digits=10, decimal_places=2)
    uom_increment = serializers.DecimalField(max_digits=10, decimal_places=2)
    category_id = serializers.IntegerField()
    subcategory_id = serializers.IntegerField()
    expiry_period = serializers.IntegerField()
    type = serializers.CharField()
    alternative_names = serializers.ListField(allow_empty=True)
    search_parameters = serializers.ListField(allow_empty=True)
    default_cost_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    offer_price = serializers.DecimalField(max_digits=10, decimal_places=2,required=False, allow_null=True)
    default_selling_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    cgst_percentage = serializers.DecimalField(max_digits=6, decimal_places=2,required=False, allow_null=True)
    sgst_percentage = serializers.DecimalField(max_digits=6, decimal_places=2,required=False, allow_null=True)
    igst_percentage = serializers.DecimalField(max_digits=6, decimal_places=2,required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True)
    seasonal_product = serializers.BooleanField()
    product_images = serializers.ListField(child=serializers.FileField(), allow_empty=True, min_length=None, max_length=None,required=False)
    sku_images = serializers.ListField()
    image_removed_ids = serializers.JSONField()
    is_admin_controlled = serializers.BooleanField()
    margin = serializers.DecimalField(max_digits=10, decimal_places=2,required=False, allow_null=True)
    delivery_charge = serializers.DecimalField(max_digits=10, decimal_places=2,required=False, allow_null=True)


class SKUStatusChangeSerializer(serializers.Serializer):
    """Serializer to Update SKU Status"""

    sku_uid = serializers.CharField()
    status = serializers.BooleanField()