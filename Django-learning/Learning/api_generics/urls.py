from django.urls import path
from .views import MovieListCreate, MovieDetail


urlpatterns = [
    path("movies/", MovieListCreate.as_view(), name="movie-list-create"),
    path("movies/<int:pk>/", MovieDetail.as_view(), name="movie-detail"),
]
