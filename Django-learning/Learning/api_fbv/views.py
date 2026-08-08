from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer


# --------------------------------------------------------------------
# STYLE 1: Function-Based Views with @api_view
# This is the MOST EXPLICIT way to write DRF APIs.
# You see every step: fetch data → serialize → return Response.
# Great for learning because there is no "magic".
# --------------------------------------------------------------------


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def book_list_create(request):
    """
    GET  /api/fbv/books/   → list all books
    POST /api/fbv/books/   → create a new book
    """
    if request.method == "GET":
        books = Book.objects.all()
        # many=True because we're serializing a QUERYSET (a list), not one object
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = BookSerializer(data=request.data)
        # is_valid() runs all the model validators — required, max_length, types...
        if serializer.is_valid():
            serializer.save()   # writes to the DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([AllowAny])
def book_detail(request, pk):
    """
    GET    /api/fbv/books/<pk>/   → read one book
    PUT    /api/fbv/books/<pk>/   → full update (all fields required)
    PATCH  /api/fbv/books/<pk>/   → partial update (only send changed fields)
    DELETE /api/fbv/books/<pk>/   → delete
    """
    book = get_object_or_404(Book, pk=pk)

    if request.method == "GET":
        serializer = BookSerializer(book)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PATCH":
        # partial=True tells the serializer "missing fields are OK"
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
