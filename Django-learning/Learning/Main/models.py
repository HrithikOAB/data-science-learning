from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=10,null=True,blank=True)
    number = models.IntegerField()
    address = models.TextField(null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    otp = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return str(self.number)
    

