# What is a Serializer? (Explained like you're 10)

## The problem

Your Django database stores stuff like a `Book` object:

```python
book = Book(title="Harry Potter", author="Rowling", price=500)
```

This is a **Python object**. Cool.

But your API sends stuff over the internet. The internet doesn't understand Python objects.
The internet speaks **JSON** — text that looks like this:

```json
{"title": "Harry Potter", "author": "Rowling", "price": 500}
```

**You need a translator.** That translator is called a **Serializer**.

## What a Serializer does

A serializer works **both ways**:

```
Python object  ──[ serializer ]──►  JSON       (going OUT to the client)
JSON           ──[ serializer ]──►  Python     (coming IN from the client)
```

- When you SEND data → serializer turns Python → JSON
- When you RECEIVE data → serializer turns JSON → Python (and checks it's valid)

That's it. That's the whole job.

## The simplest serializer

```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book              # which model?
        fields = "__all__"        # which fields to expose? all of them
```

Three lines of real code and you're done. `ModelSerializer` looks at your model and figures out the field types automatically (CharField → string, IntegerField → number, etc.).

## The two things you'll do 90% of the time

### 1. Turn Python objects into JSON (to send them out)

```python
books = Book.objects.all()                        # list of Python objects
serializer = BookSerializer(books, many=True)     # many=True because it's a LIST
return Response(serializer.data)                  # .data is the JSON-ready dict
```

**⚠️ Remember: `many=True` when it's a list. Skip it when it's one item.**

```python
book = Book.objects.get(pk=1)               # one object
serializer = BookSerializer(book)           # no many=True
return Response(serializer.data)
```

### 2. Turn incoming JSON into a database row (to save it)

```python
serializer = BookSerializer(data=request.data)    # data= means "incoming"
if serializer.is_valid():                         # runs all validations
    serializer.save()                             # writes to DB
    return Response(serializer.data, status=201)
return Response(serializer.errors, status=400)    # something was wrong
```

**Three magic methods to remember:**

| Method | What it does |
|---|---|
| `.is_valid()` | Checks all the rules (required fields, max lengths, email format...). Returns `True` or `False`. |
| `.save()` | Actually writes to the database. Only call this after `is_valid()` says True. |
| `.data` | The JSON-ready dictionary you send back. |
| `.errors` | If validation fails, this tells you WHY. Send it back with a 400 status. |

## `fields = "__all__"` vs a list

```python
fields = "__all__"                        # every field on the model
fields = ["id", "title", "author"]        # only these — hide price and stock
fields = ["id", "title"]                  # even fewer
```

You use a list when you want to **hide** some fields from the API (like passwords or internal notes).

## Update vs Create — one small trick

Same serializer, different first argument:

```python
# CREATE — no existing object
serializer = BookSerializer(data=request.data)

# UPDATE — pass the existing object first
serializer = BookSerializer(book, data=request.data)

# PARTIAL UPDATE (PATCH) — same, but add partial=True
serializer = BookSerializer(book, data=request.data, partial=True)
```

**Why `partial=True`?**
Without it, the serializer complains if you don't send every field. With it, missing fields are OK — it only updates what you sent. That's what PATCH means.

## Custom validation — when you want your own rules

`ModelSerializer` covers the basics for free. But sometimes you need extra rules like "no two students with the same name." Do that with a **second serializer just for create**, and override `create()`:

```python
class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'roll_no', 'email', 'marks']

    def create(self, validated_data):
        # extra business rules ON TOP of the built-in validation
        if Student.objects.filter(roll_no=validated_data['roll_no']).exists():
            raise serializers.ValidationError("Roll number already exists.")
        if Student.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError("Name already exists.")
        return super().create(validated_data)
```

Then use different serializers for different actions in the view:

```python
def get(self, request):
    serializer = StudentSerializer(students, many=True)     # simple one for READ
def post(self, request):
    serializer = CreateStudentSerializer(data=request.data) # strict one for CREATE
```

**Why two?** Reading data has no rules — you just return what's there. Creating data has rules — you check for duplicates, formats, etc. Splitting them keeps each serializer focused on one job. You'll see this pattern in the `api_apiview` app.

## `ModelSerializer` vs `Serializer` — 30-second version

- **`ModelSerializer`** — you have a Django model. Use this 99% of the time.
- **`Serializer`** — you don't have a model (e.g. a login form that just checks a password). You define every field by hand.

Learn `ModelSerializer` first. Skip `Serializer` until you actually need it.

## Quick recap

- Serializer = translator between **Python objects** and **JSON**.
- `ModelSerializer` builds itself from a model — cheat mode.
- `many=True` for lists. Nothing for single objects.
- `is_valid()` → `save()` → `.data` (or `.errors` if it failed).
- `partial=True` for PATCH.
- Need custom rules? Make a second serializer and override `create()`.

That's serializers. Now go read App 1. 👉
