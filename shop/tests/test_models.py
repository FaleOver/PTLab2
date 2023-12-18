from django.db.models import ManyToManyField
from djmoney.models.fields import MoneyField
from django.db.models.fields.files import ImageFieldFile
from django.test import TestCase
from shop.models import Product, Order
from datetime import datetime

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="Юбка", price=1500, image="test.jpg")
        Product.objects.create(name="Тапочки", price=700)

    def test_correctness_types(self):                   
        self.assertIsInstance(Product.objects.get(name="Юбка").name, str)
        self.assertIsInstance(Product._meta.get_field("price"), MoneyField)
        self.assertEqual(Product._meta.get_field("price").default_currency, 'RUB')
        self.assertIsInstance(Product.objects.get(name="Юбка").image, ImageFieldFile)

    def test_correctness_data(self):
        self.assertTrue(Product.objects.get(name="Юбка").price.amount == 1500)
        self.assertIsNotNone(Product.objects.get(name="Юбка").image)
        self.assertEqual(Product.objects.get(name="Юбка").image, "test.jpg")
        self.assertTrue(Product.objects.get(name="Тапочки").price.amount == 700)
        self.assertFalse(Product.objects.get(name="Тапочки").image)



class OrderTestCase(TestCase):
    def setUp(self):
        self.product_first_skirt = Product.objects.create(name="Юбка", price=1500, image="test.jpg")
        self.product_second_skirt = Product.objects.create(name="Юбка", price=1500, image="test.jpg")
        self.product_slippers = Product.objects.create(name="Тапочки", price=700)
        self.datetime = datetime.now()
        
        order = Order.objects.create(person="Ivanov", address="Svetlaya St.", discount=10, price=1980)
        order.products.add(*[self.product_first_skirt, self.product_slippers])
        
        order = Order.objects.create(person="Pavlov", address="Svetlaya St.", discount=0, price=3000)
        order.products.add(*[self.product_first_skirt, self.product_second_skirt])

    def test_correctness_types(self):
        self.assertIsInstance(Order.objects.get(person="Ivanov").person, str)
        self.assertIsInstance(Order.objects.get(person="Ivanov").address, str)
        self.assertIsInstance(Order._meta.get_field("products"), ManyToManyField)
        self.assertEqual(Order._meta.get_field("products").related_model, Product)
        self.assertIsInstance(Order.objects.get(person="Ivanov").discount, int)
        self.assertIsInstance(Order._meta.get_field("price"), MoneyField)
        self.assertEqual(Order._meta.get_field("price").default_currency, 'RUB')
        self.assertIsInstance(Order.objects.get(person="Ivanov").date, datetime)

    def test_correctness_data(self):
        self.assertTrue(Order.objects.get(person="Ivanov").address == "Svetlaya St.")
        self.assertCountEqual(Order.objects.get(person="Ivanov").products.all(),
                              [self.product_first_skirt, self.product_slippers])
        self.assertTrue(Order.objects.get(person="Ivanov").discount == 10)
        self.assertTrue(Order.objects.get(person="Ivanov").price.amount, 1980)
        self.assertTrue(Order.objects.get(person="Ivanov").date.replace(microsecond=0) == \
            self.datetime.replace(microsecond=0))
        
        self.assertTrue(Order.objects.get(person="Pavlov").address == "Svetlaya St.")
        self.assertCountEqual(Order.objects.get(person="Pavlov").products.all(),
                              [self.product_first_skirt, self.product_second_skirt])
        self.assertTrue(Order.objects.get(person="Pavlov").discount == 0)
        self.assertTrue(Order.objects.get(person="Pavlov").price.amount == 3000)
        self.assertTrue(Order.objects.get(person="Pavlov").date.replace(microsecond=0) == \
            self.datetime.replace(microsecond=0))