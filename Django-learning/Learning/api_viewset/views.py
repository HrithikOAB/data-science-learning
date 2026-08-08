from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Product
from .serializers import ProductSerializer


# --------------------------------------------------------------------
# STYLE 4: ModelViewSet + Router
# The SHORTEST way to build a full CRUD API in DRF.
# ModelViewSet bundles list + create + retrieve + update + partial_update
# + destroy into a single class. When paired with a DefaultRouter in
# urls.py, you get ALL of these endpoints automatically:
#
#   GET    /products/           → list
#   POST   /products/           → create
#   GET    /products/{pk}/      → retrieve
#   PUT    /products/{pk}/      → full update
#   PATCH  /products/{pk}/      → partial update
#   DELETE /products/{pk}/      → destroy
#
# ...plus a browsable API root at /products/  (open in a browser!)
# --------------------------------------------------------------------


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
