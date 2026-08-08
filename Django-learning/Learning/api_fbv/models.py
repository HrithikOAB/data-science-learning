from django.db import models


# --------------------------------------------------------------------
# App 1 — Function-Based Views (FBV) style
# The simplest possible model. Nothing DRF-specific here — just a Django model.
# --------------------------------------------------------------------
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    published_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
