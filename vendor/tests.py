from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer
from datetime import datetime
 
class VendorAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'test@example.com',
            'address': '123 Test St',
            'vendor_code': 'TEST123'
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)
        self.vendor_id = self.vendor.id

    def test_get_all_vendors(self):
        response = self.client.get(reverse('vendor-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vendor(self):
        response = self.client.post(reverse('vendor-list-create'), self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)

    def test_retrieve_vendor(self):
        response = self.client.get(reverse('vendor-retrieve-update-destroy', kwargs={'pk': self.vendor_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vendor(self):
        updated_data = {
            'name': 'Updated Vendor',
            'contact_details': 'updated@example.com',
            'address': '456 Updated St',
            'vendor_code': 'UPDATED456'
        }
        response = self.client.put(reverse('vendor-retrieve-update-destroy', kwargs={'pk': self.vendor_id}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, updated_data['name'])

    def test_delete_vendor(self):
        response = self.client.delete(reverse('vendor-retrieve-update-destroy', kwargs={'pk': self.vendor_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)

class PurchaseOrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com', address='123 Test St', vendor_code='TEST123')
        self.purchase_order_data = {
            'po_number': 'PO123',
            'vendor': self.vendor.id,
            'order_date': '2024-05-06T12:00:00Z',
            'delivery_date': '2024-05-10T12:00:00Z',
            'items': [{'name': 'Item 1', 'quantity': 10}],
            'status': 'completed',
            'quality_rating': 4
        }
        self.purchase_order = PurchaseOrder.objects.create(**self.purchase_order_data)
        self.purchase_order_id = self.purchase_order.id

    def test_get_all_purchase_orders(self):
        response = self.client.get(reverse('purchase-order-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_purchase_order(self):
        response = self.client.post(reverse('purchase-order-list-create'), self.purchase_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

    def test_retrieve_purchase_order(self):
        response = self.client.get(reverse('purchase-order-retrieve-update-destroy', kwargs={'pk': self.purchase_order_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_purchase_order(self):
        updated_data = {
            'po_number': 'UPDATEDPO123',
            'order_date': '2024-05-07T12:00:00Z',
            'status': 'in_progress'
        }
        response = self.client.put(reverse('purchase-order-retrieve-update-destroy', kwargs={'pk': self.purchase_order_id}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.po_number, updated_data['po_number'])
        self.assertEqual(self.purchase_order.order_date.isoformat(), updated_data['order_date'])
        self.assertEqual(self.purchase_order.status, updated_data['status'])

    def test_delete_purchase_order(self):
        response = self.client.delete(reverse('purchase-order-retrieve-update-destroy', kwargs={'pk': self.purchase_order_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)


class VendorPerformanceAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com', address='123 Test St', vendor_code='TEST123')
        self.historical_performance_data = {
            'vendor': self.vendor,
            'on_time_delivery_rate': 80.0,
            'quality_rating_avg': 4.5,
            'average_response_time': 3600.0,
            'fulfillment_rate': 90.0
        }
        self.historical_performance = HistoricalPerformance.objects.create(**self.historical_performance_data)
        self.vendor_id = self.vendor.id

    def test_retrieve_vendor_performance(self):
        response = self.client.get(reverse('vendor-performance', kwargs={'pk': self.vendor.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vendor_details']['name'], 'Test Vendor')
        self.assertEqual(response.data['performance_metrics']['on_time_delivery_rate'], self.performance_data['on_time_delivery_rate'])
        self.assertEqual(response.data['performance_metrics']['quality_rating_avg'], self.performance_data['quality_rating_avg'])
        self.assertEqual(response.data['performance_metrics']['average_response_time'], self.performance_data['average_response_time'])
        self.assertEqual(response.data['performance_metrics']['fulfillment_rate'], self.performance_data['fulfillment_rate'])