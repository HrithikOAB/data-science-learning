from rest_framework import serializers
from .models import Book


# --------------------------------------------------------------------
# What is a Serializer?
# A Serializer converts Django model instances (Python objects) into JSON
# (so the API can SEND them to the client), AND converts incoming JSON back
# into Python data that we can save into the DB.
#
# ModelSerializer is the shortcut: it looks at the model's fields and
# builds the serializer automatically. You just tell it which model and
# which fields to expose.
# --------------------------------------------------------------------
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"   # expose every field — use a list to restrict, e.g. ["id","title"]
