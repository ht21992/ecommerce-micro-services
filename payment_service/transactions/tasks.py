from celery import shared_task


@shared_task
def process_payment(order_id, amount=100):
    print(f"Processing payment for order {order_id}, amount={amount}")
    return {"success": True}  # <-- force success
