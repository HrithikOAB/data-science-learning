from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=10,null=True,blank=True)
    number = models.IntegerField()
    address = models.TextField(null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    otp = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return str(self.number)
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class whishlist(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

class PanCard(models.Model):
    user = models.OneToOneField(Person,on_delete=models.CASCADE)
    pan_number = models.CharField(max_length=10)
    full_name = models.TextField()
    image = models.ImageField(upload_to='pancard')

    def __str__(self):
        return self.full_name

  






