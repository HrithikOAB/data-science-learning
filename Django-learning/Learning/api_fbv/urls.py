from django.urls import path
from . import views


# Two URLs — one for the collection, one for a single item.
# Notice we point at FUNCTIONS directly (no .as_view()).
urlpatterns = [
    path("books/", views.book_list_create, name="book-list-create"),
    path("books/<int:pk>/", views.book_detail, name="book-detail"),
]
