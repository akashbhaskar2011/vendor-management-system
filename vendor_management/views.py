from rest_framework import generics
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer
from django.utils import timezone
from django.db.models import F, fields
from django.db.models import Avg


# for the receiver
from django.db.models.signals import post_save
from django.dispatch import receiver

# for authentication anf tokken
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view


from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vendor, HistoricalPerformance


class VendorPerformanceAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            performance_metrics = {
                "on_time_delivery_rate": vendor.on_time_delivery_rate,
                "quality_rating_avg": vendor.quality_rating_avg,
                "average_response_time": vendor.average_response_time,
                "fulfillment_rate": vendor.fulfillment_rate,
            }
            return Response(performance_metrics)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=404)


@api_view(["POST"])
def acknowledge_purchase_order(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        vendor = purchase_order.vendor
        performance_metrics = calculate_vendor_performance_matrics(vendor)
        vendor.average_response_time = performance_metrics["average_response_time"]
        vendor.save()

        return Response({"message": "Purchase order acknowledged successfully"})
    except PurchaseOrder.DoesNotExist:
        return Response({"error": "Purchase order not found"}, status=404)


@api_view(["POST"])
def generate_token(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response(
            {"error": "Please provide both username and password"}, status=400
        )

    user = authenticate(username=username, password=password)

    if not user:
        return Response({"error": "Invalid username or password"}, status=400)

    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})


class VendorListCreateApiView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


class PurchaseOrderListCreateApiView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]



class PurchaseOrdersByVendorAPIView(generics.ListAPIView):
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        vendor_id = self.kwargs["vendor_id"]
        return PurchaseOrder.objects.filter(vendor_id=vendor_id)


def calculate_vendor_performance_matrics(vendor):
    # for the on time delieery rate calculations
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status="Completed")
    total_completed_orders = completed_orders.count()
    on_time_deliveries = completed_orders.filter(
        delivery_date__lte=timezone.now()
    ).count()
    on_time_delivery_rate = (
        (on_time_deliveries / total_completed_orders) * 100
        if total_completed_orders > 0
        else 0
    )

    # for calculating qual rating
    quality_rating_sum = 0
    total_completed_orders = 0
    quality_rating_avg = 0

    for order in completed_orders:
        if order.quality_rating is not None:
            quality_rating_sum += order.quality_rating
            total_completed_orders += 1
        quality_rating_avg = (
            quality_rating_sum / total_completed_orders
            if total_completed_orders > 0
            else 0
        )

    # to check this once again
    # calculate avg response time
    acknowledged_orders = completed_orders.exclude(acknowledgment_date__isnull=True)
    total_acknowledged_orders = acknowledged_orders.count()
    average_response_time = (
        acknowledged_orders.aggregate(
            mean_response_time=Avg(
                F("acknowledgment_date") - F("issue_date"),
                output_field=fields.FloatField(),
            )
        )["mean_response_time"]
        or 0
    )

    # calculating fulfillment rate
    fulfilled_orders = completed_orders.exclude(issue_date__isnull=True).count()
    fullfilment_rate = (
        (fulfilled_orders / total_completed_orders) * 100
        if total_completed_orders > 0
        else 0
    )

    historical_performance = HistoricalPerformance(
        vendor=vendor,
        date=timezone.now(),
        on_time_delivery_rate=on_time_delivery_rate,
        quality_rating_avg=quality_rating_avg,
        average_response_time=average_response_time,
        fulfillment_rate=fullfilment_rate,
    )
    historical_performance.save()

    return {
        "on_time_delivery_rate": on_time_delivery_rate,
        "quality_rating_avg": quality_rating_avg,
        "average_response_time": (average_response_time),
        "fullfilment_rate": fullfilment_rate,
    }


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, created, **kwargs):
    if created:
        vendor = instance.vendor
        performance_metrics = calculate_vendor_performance_matrics(vendor=vendor)
        vendor.on_time_delivery_rate = performance_metrics["on_time_delivery_rate"]
        vendor.quality_rating_avg = performance_metrics["quality_rating_avg"]
        vendor.average_response_time = performance_metrics["average_response_time"]
        vendor.fulfillment_rate = performance_metrics["fullfilment_rate"]
        vendor.save()
