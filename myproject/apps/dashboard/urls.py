from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardHomeView.as_view(), name="home"),
    path("productos/", views.ProductListAdminView.as_view(), name="product_list"),
    path("productos/nuevo/", views.ProductCreateView.as_view(), name="product_create"),
    path("productos/editar/<int:pk>/", views.ProductUpdateView.as_view(), name="product_update"),
    path("productos/eliminar/<int:pk>/", views.ProductDeleteView.as_view(), name="product_delete"),
]
