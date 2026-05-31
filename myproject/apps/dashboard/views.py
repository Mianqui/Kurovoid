from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Prefetch, Q
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from catalog.models import Category, Product, ProductImage

from .forms.product import ProductForm

decorators = [login_required, staff_member_required]


@method_decorator(decorators, name="dispatch")
class DashboardHomeView(TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_products"] = Product.objects.count()
        context["total_categories"] = Category.objects.count()
        context["out_of_stock"] = Product.objects.filter(stock=0).count()
        context["low_stock"] = Product.objects.filter(stock__gt=0, stock__lte=3).count()
        context["latest_products"] = Product.objects.order_by("-created_at")[:5]
        return context


@method_decorator(decorators, name="dispatch")
class ProductListAdminView(ListView):
    model = Product
    template_name = "dashboard/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        qs = Product.objects.select_related("category").prefetch_related(
            Prefetch("images", queryset=ProductImage.objects.filter(is_main=True), to_attr="_main_images")
        )
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(name__icontains=q) | Q(category__name__icontains=q)
            )
        return qs


@method_decorator(decorators, name="dispatch")
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "dashboard/product_form.html"
    success_url = reverse_lazy("dashboard:product_list")

    def form_valid(self, form):
        messages.success(self.request, "Producto creado exitosamente.")
        return super().form_valid(form)


@method_decorator(decorators, name="dispatch")
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "dashboard/product_form.html"
    context_object_name = "product"
    success_url = reverse_lazy("dashboard:product_list")
    pk_url_kwarg = "pk"

    def get_initial(self):
        initial = super().get_initial()
        product = self.get_object()
        main_img = product.images.filter(is_main=True).first()
        if main_img:
            initial["image"] = main_img.image
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editing"] = True
        context["main_image"] = self.get_object().images.filter(is_main=True).first()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado exitosamente.")
        return super().form_valid(form)


@method_decorator(decorators, name="dispatch")
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "dashboard/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("dashboard:product_list")
    pk_url_kwarg = "pk"

    def form_valid(self, form):
        messages.success(self.request, "Producto eliminado.")
        return super().form_valid(form)
