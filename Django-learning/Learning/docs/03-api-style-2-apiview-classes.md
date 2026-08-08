# App 2 — Class-Based `APIView` (`api_apiview`)

**Same thing as App 1, but written as a class.** Each HTTP method (GET, POST, PUT...) becomes a method on the class. No more giant `if request.method == "..."` chains.

## The model

```python
# api_apiview/models.py
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    marks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
```

Two bonus fields:
- `created_at` uses `auto_now_add=True` → set **once** when the row is created.
- `updated_at` uses `auto_now=True` → refreshed **every time** you save.

You don't send these from the client. Django fills them in automatically.

## Two serializers (a small but important idea)

This app teaches something new: **you can have more than one serializer per model.** Use different ones for different jobs.

```python
# api_apiview/serializers.py

class StudentSerializer(serializers.ModelSerializer):
    """Used for READING (GET). Returns everything, no rules."""
    class Meta:
        model = Student
        fields = "__all__"


class CreateStudentSerializer(serializers.ModelSerializer):
    """Used for CREATING (POST). Enforces custom rules."""
    class Meta:
        model = Student
        fields = ['name', 'roll_no', 'email', 'marks']   # no created_at/updated_at

    def create(self, validated_data):
        # extra rules beyond the built-in validation:
        if Student.objects.filter(roll_no=validated_data['roll_no']).exists():
            raise serializers.ValidationError("A student with this roll number already exists.")
        if Student.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError("A student with this name already exists.")
        return super().create(validated_data)
```

**Why two?**
- `StudentSerializer` is for showing data. It shows every field, including timestamps.
- `CreateStudentSerializer` is for accepting data. It only lets clients send the 4 real fields (timestamps are auto), AND it blocks duplicates.

This "split serializer" pattern is very common in real projects: one for **read**, one for **write**.

## The views — two classes

### Class 1: list + create

```python
class StudentListCreate(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateStudentSerializer(data=request.data)   # note: create serializer!
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**What changed vs App 1?**
- No `@api_view` decorator — the class inherits from `APIView`.
- No `if request.method == ...` — DRF calls `get()` for GET, `post()` for POST. Cleaner.
- `permission_classes = [AllowAny]` sits on the class (not a decorator).
- Notice we use **`StudentSerializer` for read** and **`CreateStudentSerializer` for write**.

### Class 2: detail (read one / update / delete)

```python
class StudentDetail(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        # tiny helper so we don't repeat this in every method
        return get_object_or_404(Student, pk=pk)

    def get(self, request, pk):
        return Response(StudentSerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        serializer = StudentSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        serializer = StudentSerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

**The `get_object()` helper** is a nice cleanup — write it once, reuse it in every method. That's the kind of thing classes make easy.

## The URLs

```python
# api_apiview/urls.py
urlpatterns = [
    path("students/", StudentListCreate.as_view(), name="student-list-create"),
    path("students/<int:pk>/", StudentDetail.as_view(), name="student-detail"),
]
```

**Important:** with class-based views you MUST add `.as_view()`. That turns the class into a callable Django can use.

## Try it out

```bash
# Create — succeeds
curl -X POST http://127.0.0.1:8000/api/apiview/students/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Aisha","roll_no":"R001","email":"aisha@ex.com","marks":88}'

# Create again with same roll_no — blocked by our custom rule
curl -X POST http://127.0.0.1:8000/api/apiview/students/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Rita","roll_no":"R001","email":"rita@ex.com","marks":70}'
# → "A student with this roll number already exists."

# List all
curl http://127.0.0.1:8000/api/apiview/students/
```

## FBV vs APIView — when do I use which?

| Function-based (App 1) | Class-based APIView (App 2) |
|---|---|
| Very small views | Views with shared setup (like `get_object`) |
| One-off endpoints | Endpoints where you'll reuse logic |
| Beginners | Once you're comfortable with classes |

Both do the exact same thing. Class-based just scales better when your view starts growing.

**Next up:** [App 3 — Generic views (DRF writes the boring parts for you)](04-api-style-3-generic-views.md)
