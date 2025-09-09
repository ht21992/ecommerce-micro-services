from celery import shared_task


@shared_task
def reserve_stock(order_id):
    print(f"Reserving stock for order {order_id}")
    return {"success": True}  # <-- force success for now
