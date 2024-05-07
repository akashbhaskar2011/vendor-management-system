from django.db import models


# for exception validatoin
from django.core.exceptions import ValidationError


# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(unique=True, max_length=50)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name + " " + self.vendor_code

    def clean(self):
        if self.on_time_delivery_rate < 0 or self.on_time_delivery_rate > 100:
            raise ValidationError(
                "on time delivery can be grater than 0 and smaller than 100"
            )
        if self.quality_rating_avg < 0 or self.quality_rating_avg < 5:
            raise ValidationError("quality rating avg must be beween 0 and 5")


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(
        max_length=50,
        choices=(
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Canceled", "Canceled"),
        ),
    )
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.status not in ["pending", "completed", "canceled"]:
            raise ValidationError(
                "Status must be one of: 'pending', 'completed', 'canceled'."
            )


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
