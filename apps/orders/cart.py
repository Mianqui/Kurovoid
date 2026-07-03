from decimal import Decimal

from django.conf import settings

from catalog.models import Product


# Carrito de compras almacenado en sesión (sin BD)
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # Agrega un producto o incrementa su cantidad
    def add(self, product, quantity=1, size=None, color=None):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
                "size": size or "",
                "color": color or "",
            }
        self.cart[product_id]["quantity"] += quantity
        self.save()

    # Elimina un producto del carrito
    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # Actualiza la cantidad de un producto
    def update(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] = quantity
            self.save()

    # Suma total del carrito
    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    # Vacía el carrito
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def save(self):
        self.session.modified = True

    # Cantidad total de items
    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    # Itera sobre los productos con datos completos
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            item = self.cart[str(product.id)]
            item["product"] = product
            item["total_price"] = Decimal(item["price"]) * item["quantity"]
            yield item
