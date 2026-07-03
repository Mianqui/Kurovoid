from catalog.models import Product


def dashboard_sidebar(request):
    if request.user.is_authenticated and request.user.is_staff:
        return {
            "low_stock_count": Product.objects.filter(stock__lte=3).count()
        }
    return {}
