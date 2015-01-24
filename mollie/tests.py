import unittest
from mollie.api.client import Client
from mollie.api.error import Error


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.set_api_key('test_2rjdxSfxrvPei55ARwBBDipSRGsaGn')

    def test_create(self):
        try:
            payment = self.client.payments.create({
                'amount': 10.00,
                'description': 'My first API payment',
                'redirectUrl': 'http://webshop.example.org/order/12345',
                'metadata': {
                    'order_nr': '12345'
                }
            })
            self.assertTrue(payment.is_open())
            return payment

        except Error as e:
            return 'API call failed: ' + e.message

    def test_get(self):
        created_payment = self.test_create()
        payment = self.client.payments.get(created_payment.get('id'))
        self.assertEqual(created_payment.get('amount'), payment.get('amount'))
        self.assertEqual(created_payment.get('id'), payment.get('id'))
        self.assertEqual(created_payment.get('createdDatetime'), payment.get('createdDatetime'))
        return payment

    def test_refund(self):
        fetched_payment = self.test_get()
        created_payment = self.test_create()
        
        try:
            self.client.payments.refund(fetched_payment)
        except Error as e:
            if 'The payment is already refunded or has not been paid for yet.' in str(e):
                return True

        try:
            self.client.payments.refund(created_payment)
        except Error as e:
            if 'The payment is already refunded or has not been paid for yet.' in str(e):
                return True


if __name__ == '__main__':
    unittest.main()