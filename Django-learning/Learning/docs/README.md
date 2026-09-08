# DRF Tutorial — Docs for Students

Hey! This folder explains the DRF (Django REST Framework) code in this project in **super simple language**.
Read them in this order:

1. **[01-serializers-explained.md](01-serializers-explained.md)** — What is a serializer? Start here.
2. **[02-api-style-1-function-based-views.md](02-api-style-1-function-based-views.md)** — App `api_fbv` (easiest to understand)
3. **[03-api-style-2-apiview-classes.md](03-api-style-2-apiview-classes.md)** — App `api_apiview` (same thing, but as a class)
4. **[04-api-style-3-generic-views.md](04-api-style-3-generic-views.md)** — App `api_generics` (DRF does the boring stuff for us)
5. **[05-api-style-4-viewsets-router.md](05-api-style-4-viewsets-router.md)** — App `api_viewset` (the shortest way)

## Authentication (how users log in)

6. **[06-what-is-authentication.md](06-what-is-authentication.md)** — What is authentication and its types? Start here.
7. **[07-session-auth-django-templates.md](07-session-auth-django-templates.md)** — App `Main` (session/cookie login with HTML pages)
8. **[08-token-auth-drf-fbv.md](08-token-auth-drf-fbv.md)** — App `tokenAuth` (token login for APIs, using `@api_view`)

## What are we building in each app?

**The exact same thing four times.** A tiny CRUD API. Different code, same result.

CRUD = **C**reate, **R**ead, **U**pdate, **D**elete — the four things you do with data.

| HTTP method | What it does | Example |
|---|---|---|
| `GET` | Read data | "Give me all books" |
| `POST` | Create new data | "Add a new book" |
| `PUT` | Replace something completely | "Overwrite this book" |
| `PATCH` | Update one or two fields | "Just change the price" |
| `DELETE` | Remove something | "Delete this book" |

## How to run the server

```bash
cd Learning
python manage.py runserver
```

Then open these in your browser or Postman:

| App | URL |
|---|---|
| api_fbv | `http://127.0.0.1:8000/api/fbv/books/` |
| api_apiview | `http://127.0.0.1:8000/api/apiview/students/` |
| api_generics | `http://127.0.0.1:8000/api/generics/movies/` |
| api_viewset | `http://127.0.0.1:8000/api/viewset/products/` |

## The big idea

Look at how the code gets **shorter** as you go from App 1 → App 4.
That's not magic — DRF is doing more work for you each time.
By App 4 you write **3 lines** and get a full CRUD API. 🎉
