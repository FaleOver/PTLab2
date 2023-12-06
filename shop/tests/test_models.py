from django.db.models import ImageField, ManyToManyField
from django.db.models.fields.files import ImageFieldFile
from django.test import TestCase
from shop.models import Product, Order
from datetime import datetime

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="Юбка", price="1550", image="test.jpg")
        Product.objects.create(name="Тапочки", price="700")

    def test_correctness_types(self):                   
        self.assertIsInstance(Product.objects.get(name="Юбка").name, str)
        self.assertIsInstance(Product.objects.get(name="Юбка").price, int)
        self.assertIsInstance(Product.objects.get(name="Юбка").image, ImageFieldFile)
        self.assertIsInstance(Product.objects.get(name="Тапочки").name, str)
        self.assertIsInstance(Product.objects.get(name="Тапочки").price, int)
        self.assertIsInstance(Product.objects.get(name="Тапочки").image, ImageFieldFile)

    def test_correctness_data(self):
        self.assertTrue(Product.objects.get(name="Юбка").price == 1550)
        self.assertIsNotNone(Product.objects.get(name="Юбка").image)
        self.assertEqual(Product.objects.get(name="Юбка").image, "test.jpg")
        self.assertTrue(Product.objects.get(name="Тапочки").price == 700)
        self.assertFalse(Product.objects.get(name="Тапочки").image)



class OrderTestCase(TestCase):
    def setUp(self):
        self.product_skirt = Product.objects.create(name="Юбка", price="1550", image="test.jpg")
        self.product_slippers = Product.objects.create(name="Тапочки", price="700")
        self.datetime = datetime.now()
        order = Order.objects.create(person="Ivanov",
                                address="Svetlaya St.")
        order.products.add(*[self.product_skirt, self.product_slippers])

    def test_correctness_types(self):
        self.assertIsInstance(Order.objects.get(person="Ivanov").person, str)
        self.assertIsInstance(Order.objects.get(person="Ivanov").address, str)
        self.assertIsInstance(Order._meta.get_field('products'), ManyToManyField)
        self.assertEqual(Order._meta.get_field('products').related_model, Product)
        self.assertIsInstance(Order.objects.get(person="Ivanov").date, datetime)

    def test_correctness_data(self):
        self.assertTrue(Order.objects.get(person="Ivanov").person == "Ivanov")
        self.assertTrue(Order.objects.get(person="Ivanov").address == "Svetlaya St.")
        self.assertCountEqual(Order.objects.get(person="Ivanov").products.all(),
                              [self.product_skirt, self.product_slippers])
        self.assertTrue(Order.objects.get(person="Ivanov").date.replace(microsecond=0) == \
            self.datetime.replace(microsecond=0))