from .views import ChargeView, RefundView
from django.urls import path


urlpatterns = [
    path("charge/", ChargeView.as_view()),
    path("refund/", RefundView.as_view()),
]
