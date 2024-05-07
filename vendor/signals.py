from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import PurchaseOrder, HistoricalPerformance

@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, created, **kwargs):
    vendor = instance.vendor
    if instance.status == 'completed' and instance.delivery_date:
        # Calculate On-Time Delivery Rate
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_orders = completed_orders.filter(delivery_date__lte=instance.delivery_date)
        on_time_delivery_rate = (on_time_orders.count() / completed_orders.count()) * 100
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()

    if instance.quality_rating:
        # Calculate Quality Rating Average
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
        quality_rating_avg = completed_orders.aggregate(avg_rating=models.Avg('quality_rating'))['avg_rating']
        vendor.quality_rating_avg = quality_rating_avg
        vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def calculate_response_time(sender, instance, created, **kwargs):
    vendor = instance.vendor
    if instance.acknowledgment_date:
        # Calculate Average Response Time
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_orders]
        avg_response_time = sum(response_times) / len(response_times)
        vendor.average_response_time = avg_response_time
        vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def calculate_fulfilment_rate(sender, instance, created, **kwargs):
    vendor = instance.vendor
    # Calculate Fulfilment Rate
    all_orders = PurchaseOrder.objects.filter(vendor=vendor)
    fulfilled_orders = all_orders.filter(status='completed')
    fulfilment_rate = (fulfilled_orders.count() / all_orders.count()) * 100
    vendor.fulfillment_rate = fulfilment_rate
    vendor.save()

@receiver(pre_delete, sender=PurchaseOrder)
def recalculate_metrics_on_delete(sender, instance, **kwargs):
    # Recalculate metrics if a purchase order is deleted
    vendor = instance.vendor
    update_performance_metrics(sender, instance, created=False)
