from django.db import models
import uuid


class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("INVENTORY_RESERVED", "Inventory Reserved"),
        ("PAID", "Paid"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
        ("FAILED", "Failed"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.UUIDField()  # product id from inventory service
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
