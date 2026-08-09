from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Movie
from .serializers import MovieSerializer


# --------------------------------------------------------------------
# STYLE 3: Generic Class-Based Views
# Look how SHORT this is! DRF ships pre-built generic views that already
# know how to List, Create, Retrieve, Update, and Destroy.
# You just tell them:
#   1) which queryset to use
#   2) which serializer to use
# ...and DRF fills in every HTTP method for you.
#
#   ListCreateAPIView             → GET (list)   + POST (create)
#   RetrieveUpdateDestroyAPIView  → GET (one) + PUT + PATCH + DELETE
# --------------------------------------------------------------------


class MovieListCreate(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

    
