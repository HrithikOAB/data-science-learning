# App 1 — Function-Based Views (`api_fbv`)

**The most beginner-friendly style.** You write plain Python functions and decorate them with `@api_view`. No classes, no inheritance, no magic.

## The model

```python
# api_fbv/models.py
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    published_date = models.DateField(null=True, blank=True)
```

Nothing fancy — just a normal Django model.

## The serializer

```python
# api_fbv/serializers.py
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
```

If serializers still feel weird, read [`01-serializers-explained.md`](01-serializers-explained.md) first.

## The views — two functions

We need two URLs:
- `/api/fbv/books/` — the **collection** (all books, or add a new one)
- `/api/fbv/books/<id>/` — a **single** book (read/update/delete it)

So we write two functions, one for each URL.

### Function 1: list + create

```python
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def book_list_create(request):
    if request.method == "GET":
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)   # many=True for list
        return Response(serializer.data)

    if request.method == "POST":
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**What's happening:**
1. `@api_view(["GET", "POST"])` = "this function handles GET and POST, reject everything else"
2. Check `request.method` to decide what to do
3. For GET: fetch all books → serialize → return
4. For POST: read the incoming JSON → validate → save → return the new book

### Function 2: read one + update + delete

```python
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([AllowAny])
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)   # 404 automatically if not found

    if request.method == "GET":
        return Response(BookSerializer(book).data)

    if request.method == "PUT":
        serializer = BookSerializer(book, data=request.data)  # note: book passed in
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == "PATCH":
        serializer = BookSerializer(book, data=request.data, partial=True)  # partial=True
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

**Two things to notice:**
- `get_object_or_404(Book, pk=pk)` — if the book doesn't exist, Django returns 404 for you.
- `PUT` vs `PATCH` — same code, but PATCH adds `partial=True` so missing fields are OK.

## The URLs

```python
# api_fbv/urls.py
urlpatterns = [
    path("books/", views.book_list_create, name="book-list-create"),
    path("books/<int:pk>/", views.book_detail, name="book-detail"),
]
```

Just point at the **function directly** (no `.as_view()` — that's only for classes).

## Try it out

Start the server (`python manage.py runserver`) then:

```bash
# Create
curl -X POST http://127.0.0.1:8000/api/fbv/books/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Harry Potter","author":"Rowling","price":500}'

# List all
curl http://127.0.0.1:8000/api/fbv/books/

# Read one
curl http://127.0.0.1:8000/api/fbv/books/1/

# Update just the price (PATCH)
curl -X PATCH http://127.0.0.1:8000/api/fbv/books/1/ \
  -H "Content-Type: application/json" -d '{"price":600}'

# Delete
curl -X DELETE http://127.0.0.1:8000/api/fbv/books/1/
```

## Why start with this style?

- Reads top-to-bottom like a story
- No class inheritance to figure out
- You see **every step**: fetch → serialize → return
- Great for tiny APIs and quick prototypes

## Downside

- Lots of typing. Every new model = same pattern copy-pasted.
- That's what the next three styles fix.

**Next up:** [App 2 — APIView classes](03-api-style-2-apiview-classes.md)
