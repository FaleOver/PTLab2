from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    image = models.ImageField(null = True)

class Order(models.Model):
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    products = models.ManyToManyField('Product')
    date = models.DateTimeField(auto_now_add=True)