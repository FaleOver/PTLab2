from django.test import TestCase, Client

class OrderCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_accessibility(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_cart_accessibility(self):
        product_ids = "1,2,3"
        response = self.client.post('/cart/', { 'product_ids': product_ids })

        self.assertEqual(response.status_code, 200)
        
    def test_order_accessibility(self):
        person = "Ivanov"
        address = "Svetlaya St."
        product_ids = "1,2,3"

        response = self.client.post('/cart/', {
            'person': person,
            'address': address,
            'product_ids': product_ids
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('Ваш заказ оформлен. Спасибо, Ivanov!', response.content.decode())