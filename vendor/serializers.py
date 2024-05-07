from rest_framework import serializers
from .models import Vendor, PurchaseOrder
import json

#Vendor Profile Management Serializer
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'contact_details', 'address', 'vendor_code',
                  'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

#Purchase Order Tracking Serializer
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'vendor', 'order_date', 'delivery_date',
                  'items', 'quantity', 'status', 'quality_rating',
                  'issue_date', 'acknowledgment_date']
        
        def to_representation(self, instance):
            ret = super().to_representation(instance)
        # Deserialize items data from JSON
            ret['items'] = json.loads(ret['items'])
            return ret

        def to_internal_value(self, data):
            data['items'] = json.dumps(data.get('items', {}))
            return super().to_internal_value(data)