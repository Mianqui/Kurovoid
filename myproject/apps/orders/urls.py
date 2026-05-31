from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),                     # /pedidos/
    path("agregar/<int:product_id>/", views.cart_add, name="cart_add"),  # /pedidos/agregar/<id>/
    path("quitar/<int:product_id>/", views.cart_remove, name="cart_remove"),  # /pedidos/quitar/<id>/
    path("update/<int:product_id>/", views.cart_update, name="cart_update"),  # /pedidos/update/<id>/
]
