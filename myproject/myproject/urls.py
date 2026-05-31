from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from catalog.views import HomeView

# Rutas principales del proyecto
urlpatterns = [
    path("", HomeView.as_view(), name="home"),               # Página de inicio
    path("", include("users.urls")),                         # Login /logout en /login/ /logout/
    path("kurovoid-secret-admin/", admin.site.urls),         # Panel admin Django
    path("tienda/", include("catalog.urls")),                # Catálogo de productos
    path("pedidos/", include("orders.urls")),                # Carrito y pedidos
    path("dashboard/", include("dashboard.urls")),           # Panel staff/superuser
]

# Sirve archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
