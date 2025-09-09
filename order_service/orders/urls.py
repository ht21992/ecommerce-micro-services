from django.urls import path
from .views import CreateOrderView, OrderDetailView

urlpatterns = [
    path("orders/", CreateOrderView.as_view(), name="order-create"),
    path("orders/<uuid:order_id>/", OrderDetailView.as_view(), name="order-detail"),
]
