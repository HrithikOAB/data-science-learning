from django.db import models


# --------------------------------------------------------------------
# App 4 — ModelViewSet + Router
# A separate Product model just for this tutorial app (do not confuse
# with Main.Product — different tables, different apps).
# --------------------------------------------------------------------
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name
