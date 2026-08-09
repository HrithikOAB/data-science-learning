from django.urls import path
from . import views


# Two URLs — one for the collection, one for a single item.
# Notice we point at FUNCTIONS directly (no .as_view()).
urlpatterns = [
    path("books/", views.create_book_entry, name="book-list"),
    # path("create_book/", views.create_book_entry, name="create-book"),


    path("books/<int:pk>/", views.book_detail, name="book-detail"),
]
