from django.conf import settings
from django.db import models

from catalog.models import Product


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("confirmado", "Confirmado"),
        ("enviado", "Enviado"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    nombre_cliente = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion_envio = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="pendiente")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    numero_guia = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["-creado_en"]

    def numero_pedido(self):
        h = hex(self.id)[2:].upper().zfill(4)
        return f"KRV-{h}"

    def __str__(self):
        return f"{self.numero_pedido()} - {self.get_estado_display()}"


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField(default=1)
    talla = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=50, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.name} x{self.cantidad}"
