from django.db import models
import uuid


class Shipment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("reserved", "Reserved"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    order_id = models.IntegerField()
    customer_id = models.IntegerField()
    address = models.TextField()
    tracking_number = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipment #{self.tracking_number} - {self.status}"
