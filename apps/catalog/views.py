from django.db.models import Min, Max
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from .models import Category, Color, Product, Size, CarouselImage


# Lista de productos con filtros y paginación
class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related("category")
        # Filtros desde GET
        category_slug = self.request.GET.get("category")
        size_name = self.request.GET.get("size")
        color_name = self.request.GET.get("color")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        # Filtro de favoritos (IDs enviados desde cookie via JS)
        fav_ids = self.request.GET.get("fav_ids")
        if self.request.GET.get("favs") and fav_ids:
            try:
                ids = [int(i) for i in fav_ids.split(",") if i.strip()]
                qs = qs.filter(id__in=ids)
            except (ValueError, TypeError):
                pass
        elif self.request.GET.get("favs"):
            qs = qs.none()
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if size_name:
            qs = qs.filter(sizes__name=size_name)
        if color_name:
            qs = qs.filter(colors__name=color_name)
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)
        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Datos para filtros en sidebar
        context["categories"] = Category.objects.all()
        context["sizes"] = Size.objects.all()
        context["colors"] = Color.objects.all()
        context["price_range"] = Product.objects.filter(is_active=True).aggregate(
            min_price=Min("price"), max_price=Max("price")
        )
        context["selected"] = {
            k: v for k, v in self.request.GET.items() if v
        }
        return context


# Vista detalle de un producto por slug
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["images"] = product.images.all()
        context["categories"] = Category.objects.all()
        context["sizes"] = Size.objects.all()
        context["colors"] = Color.objects.all()
        context["price_range"] = Product.objects.filter(is_active=True).aggregate(
            min_price=Min("price"), max_price=Max("price")
        )
        context["selected"] = {}
        # Productos de la misma categoría (excluyendo el actual)
        context["related_products"] = Product.objects.filter(
            category=product.category, is_active=True
        ).exclude(id=product.id)[:4]
        return context


# Productos filtrados por categoría (slug en URL)
class CategoryView(ListView):
    model = Product
    template_name = "catalog/category_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_category(self):
        return get_object_or_404(Category, slug=self.kwargs["slug"])

    def get_queryset(self):
        return Product.objects.filter(
            category=self.get_category(), is_active=True
        ).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.get_category()
        context["categories"] = Category.objects.all()
        context["sizes"] = Size.objects.all()
        context["colors"] = Color.objects.all()
        context["price_range"] = Product.objects.filter(is_active=True).aggregate(
            min_price=Min("price"), max_price=Max("price")
        )
        context["selected"] = {}
        return context


# Página principal con categorías y últimos productos
class HomeView(TemplateView):
    template_name = "catalog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["sizes"] = Size.objects.all()
        context["colors"] = Color.objects.all()
        context["price_range"] = Product.objects.filter(is_active=True).aggregate(
            min_price=Min("price"), max_price=Max("price")
        )
        context["selected"] = {
            k: v for k, v in self.request.GET.items() if v
        }
        context["new_products"] = Product.objects.filter(is_active=True).order_by(
            "-created_at"
        )[:8]
        context["carousel_images"] = CarouselImage.objects.filter(is_active=True)
        return context
