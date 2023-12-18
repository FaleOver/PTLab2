from itertools import product
from os import name
from django.test import TestCase, Client
from django.http import HttpResponse
from shop.models import Product
from decimal import Decimal


class OrderCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.created_product_ids = []
        for _ in range(2):
            product = Product.objects.create(name="Юбка", price=500, image="test.jpg")
            self.created_product_ids.append(product.id)
        product = Product.objects.create(name="Шапка", price=1000, image="test.jpg")
        self.created_product_ids.append(product.id)

    def test_index_accessibility(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_cart_accessibility(self):
        product_ids = '1,2,3'
        response = self.client.post('/cart/', { 'product_ids': product_ids })

        self.assertEqual(response.status_code, 200)
        
    def test_empty_cart(self):
        response = self.client.post('/cart/')
        
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Неизвестный запрос', response.content.decode('utf-8'))

    def test_order_zero_discount(self):
        person = 'Ivanov'
        address = 'Svetlaya St.'
        product_ids = (str(self.created_product_ids[0]))
        total_price = Product.objects.get(id=product_ids).price
        
        response = self.client.post('/cart/', {
            'person': person,
            'address': address,
            'product_ids': product_ids
        })

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Ваш заказ оформлен. Спасибо, {0}! '.format(person) +
                         'Итоговая цена {0}'.format(total_price),
                         response.content.decode('utf-8'))
        
        products = Product.objects.filter(name="Юбка")
        product_ids = ','.join(str(product.id) for product in products)
        total_price = sum(product.price for product in products)
        
        response = self.client.post('/cart/', {
            'person': person,
            'address': address,
            'product_ids': product_ids
        })

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Ваш заказ оформлен. Спасибо, {0}! '.format(person) +
                         'Итоговая цена {0}'.format(total_price),
                         response.content.decode('utf-8'))
        
    def test_order_ten_discount(self):
        person = 'Ivanov'
        address = 'Svetlaya St.'
        product_ids = ','.join(str(product_id) for product_id in self.created_product_ids)
        total_price = sum(product.price for product in Product.objects.filter(id__in=self.created_product_ids))
        total_price -= total_price * (10 / 100)
        
        response = self.client.post('/cart/', {
            'person': person,
            'address': address,
            'product_ids': product_ids
        })

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Ваш заказ оформлен. Спасибо, {0}! '.format(person) +
                         'Cо скидкой в 10% получится всего {0}'.format(total_price),
                         response.content.decode('utf-8'))
        
    def test_empty_order(self):
        person = 'Ivanov'
        address = 'Svetlaya St.'    

        response = self.client.post('/cart/', {
            'person': person,
            'address': address,
            'product_ids': ''
        })
        
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Неверно заполнена форма', response.content.decode('utf-8'))
        
    def test_error_order(self):
            person = 'Ivanov'
            address = 'Svetlaya St.'
        
            # Максимальное значение id из Product
            max_id = max(self.created_product_ids)
            non_existing_id = max_id + 1

            response = self.client.post('/cart/', {
                'person': person,
                'address': address,
                'product_ids': non_existing_id
            })
        
            self.assertIsInstance(response, HttpResponse)
            self.assertEqual(response.status_code, 200)
            self.assertEqual('Неверно заполнена форма', response.content.decode('utf-8'))
