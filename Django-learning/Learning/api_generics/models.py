from django.db import models


# --------------------------------------------------------------------
# App 3 — Generic class-based views
# --------------------------------------------------------------------
class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)
    rating = models.FloatField(default=0.0)
    release_year = models.IntegerField()

    def __str__(self):
        return self.title
