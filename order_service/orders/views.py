from rest_framework.views import APIView
from django.views import View
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from .tasks import orchestrate_order
import uuid
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class CreateOrderView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(status="PENDING")
        # trigger saga orchestrator as Celery async
        orchestrate_order.delay(str(order.id))
        return Response({"order_id": str(order.id)}, status=status.HTTP_201_CREATED)


class OrderDetailView(View):
    def get(self, request, order_id):
        """
        Get order status by ID.
        """
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise Http404("Order not found")

        return JsonResponse(
            {
                "order_id": str(order.id),
                "status": order.status,
            }
        )
