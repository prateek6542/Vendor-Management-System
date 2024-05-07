from rest_framework import generics, status
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer,PurchaseOrderSerializer
import json
from rest_framework.response import Response

#Vendor Profile Management
class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

#Purchase Order Tracking
class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    
    def create(self, request, *args, **kwargs):
        items_data = request.data.get('items')
        # Serialize items data to JSON
        items_json = json.dumps(items_data)
        request.data['items'] = items_json
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        items_data = request.data.get('items')
        # Serialize items data to JSON
        items_json = json.dumps(items_data)
        request.data['items'] = items_json
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    
class PurchaseOrderAcknowledgeAPIView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.acknowledgment_date = timezone.now()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
#Vendor Performance Evaluation
class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        performance_metrics = HistoricalPerformance.objects.filter(vendor=instance)
        serializer = self.get_serializer(instance)
        return Response({
            'vendor_details': serializer.data,
            'performance_metrics': {
                'on_time_delivery_rate': performance_metrics.on_time_delivery_rate if performance_metrics else 0,
                'quality_rating_avg': performance_metrics.quality_rating_avg if performance_metrics else 0,
                'average_response_time': performance_metrics.average_response_time if performance_metrics else 0,
                'fulfillment_rate': performance_metrics.fulfillment_rate if performance_metrics else 0,
            }
        })    