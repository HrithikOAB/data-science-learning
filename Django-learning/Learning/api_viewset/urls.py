from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet


# The router builds the URL patterns for us. Just register the viewset
# under a prefix ("products") and it wires up every CRUD endpoint,
# including the browsable API root page.
router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
]
