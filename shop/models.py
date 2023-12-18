from django.db import models
from djmoney.models.fields import MoneyField

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='RUB')
    image = models.ImageField(null = True)

class Order(models.Model):
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    products = models.ManyToManyField('Product')
    discount = models.PositiveIntegerField(null = True)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='RUB')
    date = models.DateTimeField(auto_now_add=True)