from .views import ReserveView, ReleaseView, list_products
from django.urls import path


urlpatterns = [
    path("reserve/", ReserveView.as_view()),
    path("release/", ReleaseView.as_view()),
    path("products/", list_products, name="list-products"),
]
