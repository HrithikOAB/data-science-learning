from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=10)
    number = models.IntegerField()
    address = models.TextField()
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name