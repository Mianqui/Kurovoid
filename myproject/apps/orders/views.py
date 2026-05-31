from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from catalog.models import Product

from .cart import Cart


# Página del carrito
def cart_detail(request):
    cart = Cart(request)
    return render(request, "orders/cart_detail.html", {"cart": cart})


# Agrega producto vía POST (AJAX)
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get("quantity", 1))
    size = request.POST.get("size", "")
    color = request.POST.get("color", "")
    cart.add(product, quantity, size, color)
    return JsonResponse(
        {
            "success": True,
            "cart_total": str(cart.get_total_price()),
            "cart_count": len(cart),
        }
    )


# Elimina producto vía POST (AJAX)
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return JsonResponse(
        {
            "success": True,
            "cart_total": str(cart.get_total_price()),
            "cart_count": len(cart),
        }
    )


# Actualiza cantidad vía POST (AJAX)
@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    quantity = int(request.POST.get("quantity", 1))
    if quantity > 0:
        cart.update(product_id, quantity)
    else:
        cart.remove(product_id)
    return JsonResponse(
        {
            "success": True,
            "cart_total": str(cart.get_total_price()),
            "cart_count": len(cart),
        }
    )
