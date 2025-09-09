# inventory/products/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Reservation
from django.db import transaction
from django.http import JsonResponse


class ReserveView(APIView):
    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))
        order_id = request.data.get("order_id")
        try:
            with transaction.atomic():
                # Select for update to avoid race condition
                p = Product.objects.select_for_update().get(id=product_id)
                if p.stock < quantity:
                    return Response(
                        {"reserved": False, "reason": "out_of_stock"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                p.stock -= quantity
                p.save()
                r = Reservation.objects.create(
                    product=p, quantity=quantity, order_id=order_id
                )
                return Response(
                    {"reserved": True, "reservation_id": str(r.id)},
                    status=status.HTTP_200_OK,
                )
        except Product.DoesNotExist:
            return Response(
                {"reserved": False, "reason": "no_product"},
                status=status.HTTP_404_NOT_FOUND,
            )


# Release endpoint (compensation)
class ReleaseView(APIView):
    def post(self, request):
        reservation_id = request.data.get("reservation_id")
        order_id = request.data.get("order_id")
        try:
            with transaction.atomic():
                # Select for update to avoid race condition
                r = Reservation.objects.select_for_update().get(id=reservation_id)
                p = r.product
                p.stock += r.quantity
                p.save()
                r.delete()
                return Response({"released": True})
        except Reservation.DoesNotExist:
            return Response(
                {"released": False, "reason": "not_found"},
                status=status.HTTP_404_NOT_FOUND,
            )


def list_products(request):
    """
    Return all products with their current stock.
    """
    products = Product.objects.all()
    data = [
        {
            "id": str(p.id),
            "name": p.name,
            "stock": p.stock,
        }
        for p in products
    ]
    return JsonResponse(data, safe=False)
