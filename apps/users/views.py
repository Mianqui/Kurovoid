from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .email_utils import enviar_email_verificacion
from .models import Profile


class CustomLoginView(LoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return "/dashboard/"
        return "/tienda/"


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("users:login")


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.profile.generar_token_verificacion()
        enviar_email_verificacion(self.object, self.request)
        messages.success(
            self.request,
            f"Cuenta creada. Te enviamos un enlace de verificación a {self.object.email}.",
        )
        return response


@login_required
def verificar_email_view(request, token):
    try:
        profile = Profile.objects.get(token_verificacion=token)
    except Profile.DoesNotExist:
        messages.error(request, "El enlace de verificación no es válido.")
        return redirect("home")

    if profile.user != request.user:
        messages.error(request, "Este enlace no corresponde a tu cuenta.")
        return redirect("home")

    if not profile.token_es_valido():
        messages.warning(
            request,
            "El enlace expiró. Te enviamos uno nuevo a tu correo.",
        )
        enviar_email_verificacion(profile.user, request)
        return redirect("cuenta")

    profile.verificar_email()
    messages.success(request, "¡Correo verificado! Ya puedes realizar pedidos.")
    return redirect("cuenta")


@login_required
def cuenta_view(request):
    return render(request, "cuenta/mi_cuenta.html")


@login_required
def reenviar_verificacion_view(request):
    profile = request.user.profile
    if profile.email_verificado:
        messages.info(request, "Tu correo ya está verificado.")
        return redirect("cuenta")

    enviar_email_verificacion(request.user, request)
    messages.success(
        request,
        f"Te enviamos un nuevo enlace a {request.user.email}. Revisa también tu carpeta de spam.",
    )
    return redirect("cuenta")
