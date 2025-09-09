# payment/transactions/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transaction
import uuid


class ChargeView(APIView):
    def post(self, request):
        amount = request.data.get("amount")
        # Simulate failure if amount contains some pattern, or randomize
        if request.data.get("simulate_failure"):
            return Response({"charged": False, "reason": "card_declined"}, status=400)
        tx = Transaction.objects.create(
            order_id=request.data.get("order_id"), amount=amount, status="CHARGED"
        )
        return Response({"charged": True, "transaction_id": str(tx.id)}, status=200)


# Refund endpoint
class RefundView(APIView):
    def post(self, request):
        tx_id = request.data.get("transaction_id")
        try:
            tx = Transaction.objects.get(id=tx_id)
            tx.status = "REFUNDED"
            tx.save()
            return Response({"refunded": True})
        except Transaction.DoesNotExist:
            return Response({"refunded": False, "reason": "tx_not_found"}, status=404)
