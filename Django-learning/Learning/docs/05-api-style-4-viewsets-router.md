# App 4 — `ModelViewSet` + Router (`api_viewset`)

**The final boss. The shortest CRUD API you can write in DRF.** One class + two lines of URL config = full CRUD with a browsable API.

## The model

```python
# api_viewset/models.py
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
```

## The serializer

```python
# api_viewset/serializers.py
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
```

## The view — ONE class, three lines

```python
# api_viewset/views.py
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
```

Yes, really. **Three lines.** You get every CRUD operation.

## What's the difference vs App 3?

In App 3 we wrote **two** generic view classes (one for the list, one for the detail).
In App 4 we write **one** `ModelViewSet` class — it handles BOTH the list and the detail together.

`ModelViewSet` bundles all six of these into one class:

| Action name | HTTP → URL |
|---|---|
| `list` | GET `/products/` |
| `create` | POST `/products/` |
| `retrieve` | GET `/products/{id}/` |
| `update` | PUT `/products/{id}/` |
| `partial_update` | PATCH `/products/{id}/` |
| `destroy` | DELETE `/products/{id}/` |

## The URLs — meet the Router

This is where App 4 really shines. Instead of writing `path(...)` lines yourself, you let DRF's **router** build them for you.

```python
# api_viewset/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
]
```

**What the router did for you:**
- Wired up all 6 URLs above
- Gave you a nice **browsable API root** at `/api/viewset/` (open it in a browser!)
- Handled `.json` / `.api` format suffixes automatically

## Try it out

```bash
# Create
curl -X POST http://127.0.0.1:8000/api/viewset/products/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Notebook","category":"Stationery","price":120,"stock":30}'

# List
curl http://127.0.0.1:8000/api/viewset/products/

# Read one
curl http://127.0.0.1:8000/api/viewset/products/1/

# Update only stock
curl -X PATCH http://127.0.0.1:8000/api/viewset/products/1/ \
  -H "Content-Type: application/json" -d '{"stock":25}'

# Delete
curl -X DELETE http://127.0.0.1:8000/api/viewset/products/1/
```

**Best part:** open **`http://127.0.0.1:8000/api/viewset/products/`** in a browser. You'll see DRF's beautiful browsable HTML page where you can POST/PATCH/DELETE by filling in a form. Fantastic for testing without Postman.

## Adding custom actions to a ViewSet (bonus)

Sometimes you want an endpoint that isn't standard CRUD, like "mark this product out of stock." Use `@action`:

```python
from rest_framework.decorators import action
from rest_framework.response import Response

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'])
    def mark_out_of_stock(self, request, pk=None):
        product = self.get_object()
        product.stock = 0
        product.save()
        return Response({"status": "out of stock"})
```

The router auto-creates a URL for it: `POST /api/viewset/products/1/mark_out_of_stock/` 🎉

## The whole story in one table

| Style | Lines of view code | Complexity | When to use |
|---|---|---|---|
| **1. FBV** `@api_view` | ~35 | Very simple to read | Learning, tiny APIs |
| **2. APIView class** | ~40 | Cleaner organization | When you want shared helpers |
| **3. Generics** | ~10 | Almost nothing | 80% of real projects |
| **4. ViewSet + Router** | ~5 | Slightly magical | Standard CRUD across many models |

**All four apps do exactly the same thing.** That's the point. Now you know four ways to build a CRUD API in DRF and can pick the right tool for the job. 🚀

## Going back?

- [Intro / Index](README.md)
- [Serializers explained](01-serializers-explained.md)
- [App 1 — Function-based views](02-api-style-1-function-based-views.md)
- [App 2 — APIView classes](03-api-style-2-apiview-classes.md)
- [App 3 — Generic views](04-api-style-3-generic-views.md)
