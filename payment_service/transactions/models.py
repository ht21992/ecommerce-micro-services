from django.db import models
import uuid


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.UUIDField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=32)  # CHARGED / REFUNDED / FAILED
    created_at = models.DateTimeField(auto_now_add=True)
