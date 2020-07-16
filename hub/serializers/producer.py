import os
from django.conf import settings
from rest_framework import serializers
from datetime import datetime


class ProducersListGetSerializer(serializers.Serializer):
    """Serializer for producer list"""

    id = serializers.IntegerField()
    uid = serializers.CharField()
    name = serializers.CharField()
    franchisee__uid = serializers.CharField()
    sku_count = serializers.IntegerField()
    is_disabled = serializers.BooleanField()


class ProducerDetailsGetSerializer(serializers.Serializer):
    """Serializer for the producer details"""

    name = serializers.CharField()
    user__username = serializers.CharField()
    uid = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()
    longitude = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    is_listed = serializers.BooleanField()
    is_disabled = serializers.BooleanField()
    franchisee__name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    profile_pic__path = serializers.SerializerMethodField()    

    def get_latitude(self, obj):

        if obj['location'] not in [None]:
            return obj['location'].y
        else:
            return ''

    def get_longitude(self, obj):

        if obj['location'] not in [None]:
            return obj['location'].x
        else:
            return ''
    def get_profile_pic__path(self,obj):
        
        media_url = settings.MEDIA_URL
        if obj['profile_pic__path'] not in ['',None]:
            image = media_url+str(obj['profile_pic__path'])
            return image
        else:
            return None

class SKUListGetSerializer(serializers.Serializer):
    """Serializer to get sku List for a specific producer"""
    id = serializers.IntegerField()
    sku__id = serializers.IntegerField()
    sku__uid = serializers.CharField()
    sku__name = serializers.CharField()
    sku__sub_category__name = serializers.CharField()
    sku__category__name = serializers.CharField()
    cost_price = serializers.IntegerField()
    is_disabled = serializers.BooleanField()


class SKUDetailSerializer(serializers.Serializer):
    """Serializer for the producer SKU details"""

    id = serializers.IntegerField()
    producer_name = serializers.CharField()
    franchisee = serializers.CharField()
    sku__uom__name = serializers.CharField()
    sku_name = serializers.CharField()
    cost_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    sku_category = serializers.CharField()
    sku_sub_category = serializers.CharField()
    sku_type = serializers.CharField()
    alternative_names_list = serializers.SerializerMethodField()
    description = serializers.CharField(required=False, allow_blank=True)
    image = serializers.SerializerMethodField()
    is_disabled = serializers.BooleanField()

    def get_alternative_names_list(self,obj):
        if obj['alternate_names'] not in [None,'',[]]:
            return obj['alternate_names'][0].split(',')
        else:
            return []

    def get_image(self,obj):
        media_url = settings.MEDIA_URL
        image = media_url+str(obj['image'].path)
        return image



class PredicedStockSerializer(serializers.Serializer):
    """Serializer for producer predicted stock list"""

    id = serializers.IntegerField()
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    status = serializers.SerializerMethodField()

    def get_start_date(self, obj):
        start_date = ''
        if obj['start_date']:
            start_date = datetime.strftime(obj['start_date'],'%d/%m/%Y')
        return start_date

    def get_end_date(self, obj):
        end_date = ''
        if obj['end_date']:
            end_date = datetime.strftime(obj['end_date'],'%d/%m/%Y')
        return end_date

    def get_status(self, obj):
        status = ''
        if obj['end_date'] < datetime.now().date():
            status = 'Expired'
        if  obj['start_date'] >= datetime.now().date() or obj['end_date'] >= datetime.now().date():
            status = 'Upcoming'
        if  obj['start_date'] <= datetime.now().date() and obj['end_date'] >= datetime.now().date():
            status = 'Running'
        return status


class ProducerSKUProcurementListSerializer(serializers.Serializer):
    """Serialzier to get list of ProducerSKUProcurements"""

    sku_name = serializers.CharField()
    sku_uid = serializers.CharField()
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    expected = serializers.DecimalField(max_digits=10, decimal_places=2)
    procurement_date = serializers.DateField(format="%d %b %Y")
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)


class ProducerImageListSerializer(serializers.Serializer):
    """Serializer to get producer images"""
    id = serializers.IntegerField()
    image = serializers.SerializerMethodField()

    def get_image(self,obj):
        media_url = settings.MEDIA_URL
        if obj.image:
            image = media_url+str(obj.image.path)
        return image

class ProducerVideoListSerializer(serializers.Serializer):
    """Serializer to get producer videos"""
    id = serializers.IntegerField()
    video = serializers.SerializerMethodField()

    def get_video(self,obj):
        media_url = settings.MEDIA_URL
        if obj.video:
            video = media_url+str(obj.video.path)
        return video