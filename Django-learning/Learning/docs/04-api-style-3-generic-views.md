# App 3 — Generic Class-Based Views (`api_generics`)

**Now DRF starts doing the work for us.** In App 1 and App 2 you wrote all the CRUD logic by hand. In App 3, DRF gives you **pre-built classes** that already know how to List, Create, Retrieve, Update, and Delete. You just plug in the queryset and the serializer.

## The model

```python
# api_generics/models.py
class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)
    rating = models.FloatField(default=0.0)
    release_year = models.IntegerField()
```

## The serializer

```python
# api_generics/serializers.py
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"
```

Same as before.

## The views — hold on to your chair

```python
# api_generics/views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Movie
from .serializers import MovieSerializer


class MovieListCreate(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]
```

**That's it. That's the whole view file.** 🤯

Compare that with App 1 or App 2 — dozens of lines. Same functionality.

## What's happening?

DRF ships two ready-made classes:

| Generic view | What it handles |
|---|---|
| `ListCreateAPIView` | GET (list) + POST (create) |
| `RetrieveUpdateDestroyAPIView` | GET (one) + PUT + PATCH + DELETE |

You tell each one:
1. `queryset` — where to get the data from
2. `serializer_class` — how to translate it
3. `permission_classes` — who can access it

DRF fills in ALL the GET/POST/PUT/PATCH/DELETE methods for you, using code that looks basically like what you wrote in App 2.

## The URLs

```python
# api_generics/urls.py
urlpatterns = [
    path("movies/", MovieListCreate.as_view(), name="movie-list-create"),
    path("movies/<int:pk>/", MovieDetail.as_view(), name="movie-detail"),
]
```

Same as App 2 — `.as_view()` because it's a class.

## Try it out

```bash
curl -X POST http://127.0.0.1:8000/api/generics/movies/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Inception","genre":"Sci-Fi","rating":8.8,"release_year":2010}'

curl http://127.0.0.1:8000/api/generics/movies/
curl -X PATCH http://127.0.0.1:8000/api/generics/movies/1/ \
  -H "Content-Type: application/json" -d '{"rating":9.0}'
curl -X DELETE http://127.0.0.1:8000/api/generics/movies/1/
```

## The full family of generic views (bonus knowledge)

Sometimes you only want SOME operations, not all. DRF has one for every combo:

| Class | What it does |
|---|---|
| `ListAPIView` | Only GET (list) — read-only list |
| `CreateAPIView` | Only POST — create-only |
| `RetrieveAPIView` | Only GET one — read-only detail |
| `UpdateAPIView` | Only PUT / PATCH |
| `DestroyAPIView` | Only DELETE |
| `ListCreateAPIView` | List + Create ✅ we used this |
| `RetrieveUpdateAPIView` | Read one + update (no delete) |
| `RetrieveDestroyAPIView` | Read one + delete (no update) |
| `RetrieveUpdateDestroyAPIView` | Read one + update + delete ✅ we used this |

Pick the one that matches what you want to allow.

## Overriding when you need custom behavior

Sometimes the defaults aren't enough. You can override methods:

```python
class MovieListCreate(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_queryset(self):
        # only show highly-rated movies
        return Movie.objects.filter(rating__gte=8.0)

    def perform_create(self, serializer):
        # do something extra when saving
        serializer.save(added_by=self.request.user)
```

You get 90% of the code for free and only write the 10% that's actually unique to your app.

## When to use generic views

- ✅ When your CRUD is "normal" — fetch by pk, save with a serializer, list all
- ✅ 80% of real-world API views
- ❌ When you have really custom logic that doesn't fit the CRUD shape

**Next up:** [App 4 — ViewSets + Routers (the shortest of them all)](05-api-style-4-viewsets-router.md)
