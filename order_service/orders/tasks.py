from celery import shared_task
import requests
from django.conf import settings
from orders.models import Order

INVENTORY_URL = "http://inventory:8000/api/reserve/"
PAYMENT_URL = "http://payment:8000/api/charge/"
INVENTORY_RELEASE_URL = "http://inventory:8000/api/release/"
PAYMENT_REFUND_URL = "http://payment:8000/api/refund/"


@shared_task(name="orders.tasks.orchestrate_order", bind=True, max_retries=3)
def orchestrate_order(self, order_id):
    order = Order.objects.get(id=order_id)
    order.status = "PENDING"
    order.save()

    # 1) Reserve inventory
    try:
        resp = requests.post(
            INVENTORY_URL,
            json={
                "order_id": order_id,
                "product_id": str(order.product_id),
                "quantity": order.quantity,
            },
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
        if not data.get("reserved"):
            # inventory failed
            order.status = "CANCELLED"
            order.save()
            return {"status": "inventory_failed", "reason": data.get("reason")}
        reservation_id = data.get("reservation_id")
        order.status = "INVENTORY_RESERVED"
        order.save()
    except Exception as exc:
        order.status = "FAILED"
        order.save()
        raise self.retry(exc=exc, countdown=5)

    # 2) Charge payment
    try:
        resp = requests.post(
            PAYMENT_URL,
            json={
                "order_id": order_id,
                "amount": str(order.amount),
                "payment_method": {"type": "mock", "card": "xxxx"},
            },
            timeout=10,
        )
        resp.raise_for_status()
        pdata = resp.json()
        if not pdata.get("charged"):
            # Payment failed -> compensate inventory
            requests.post(
                INVENTORY_RELEASE_URL,
                json={"reservation_id": reservation_id, "order_id": order_id},
                timeout=5,
            )
            order.status = "CANCELLED"
            order.save()
            return {"status": "payment_failed", "reason": pdata.get("reason")}
        transaction_id = pdata.get("transaction_id")
        order.status = "PAID"
        order.save()
    except Exception as exc:
        # try to release reservation
        try:
            requests.post(
                INVENTORY_RELEASE_URL,
                json={"reservation_id": reservation_id, "order_id": order_id},
                timeout=5,
            )
        except Exception:
            pass
        order.status = "FAILED"
        order.save()
        raise self.retry(exc=exc, countdown=5)

    # success
    order.status = "COMPLETED"
    order.save()
    return {"status": "completed"}
