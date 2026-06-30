from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("registro/", views.RegisterView.as_view(), name="register"),
    path(
        "cuenta/verificar-email/<uuid:token>/",
        views.verificar_email_view,
        name="verificar_email",
    ),
    path(
        "cuenta/reenviar-verificacion/",
        views.reenviar_verificacion_view,
        name="reenviar_verificacion",
    ),
]
