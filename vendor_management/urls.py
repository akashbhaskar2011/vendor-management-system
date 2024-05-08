from django.contrib import admin
from django.urls import path
from .views import (
    VendorListCreateApiView,
    PurchaseOrderListCreateApiView,
    VendorRetrieveUpdateDestroyAPIView,
    PurchaseOrderRetrieveUpdateDestroyAPIView,
    PurchaseOrdersByVendorAPIView,
    acknowledge_purchase_order,
    VendorPerformanceAPIView,
    generate_token,
)

urlpatterns = [
    path("api/vendors/", VendorListCreateApiView.as_view(), name="vendor-list-create"),
    path("api/generate_token/", generate_token, name="generate_token"),
    path(
        "api/vendors/<int:pk>/",
        VendorRetrieveUpdateDestroyAPIView.as_view(),
        name="vendor details ",
    ),
    path(
        "api/purchase_orders/",
        PurchaseOrderListCreateApiView.as_view(),
        name="purchase-order-list-create",
    ),
    path(
        "api/purchase_orders/<int:pk>/",
        PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(),
        name="purchase details",
    ),
    # extra feature
    path(
        "api/vendors/<int:vendor_id>/purchase_orders/",
        PurchaseOrdersByVendorAPIView.as_view(),
        name="purchase-orders-by-vendor",
    ),
    path(
        "api/vendors/<int:vendor_id>/performance/",
        VendorPerformanceAPIView.as_view(),
        name="vendor-performance",
    ),
    path(
        "api/purchase_orders/<int:po_id>/acknowledge/",
        acknowledge_purchase_order,
        name="acknowledge-purchase-order",
    ),
]
