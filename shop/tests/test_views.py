from django.test import TestCase, Client
from django.http import HttpResponse
from shop.models import Product


class OrderCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.created_product_ids = []
        for _ in range(3):
            product = Product.objects.create(name="Юбка", price=500, image="test.jpg")
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

    def test_order_accessibility(self):
        person = 'Ivanov'
        address = 'Svetlaya St.'
        product_ids = ','.join(str(pid) for pid in self.created_product_ids)

        response = self.client.post('/cart/', {
            'person': person,
            'address': address,
            'product_ids': product_ids
        })

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Ваш заказ оформлен. Спасибо, Ivanov! Сумма составляет 1500.00, ' +
                         'но со скидкой получится всего 1350.00', response.content.decode())
        
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
            non_existing_id = max_id + 1 if max_id is not None else 1

            response = self.client.post('/cart/', {
                'person': person,
                'address': address,
                'product_ids': non_existing_id
            })
        
            self.assertIsInstance(response, HttpResponse)
            self.assertEqual(response.status_code, 200)
            self.assertEqual('Неверно заполнена форма', response.content.decode('utf-8'))
