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

        except Error as e:
            return 'API call failed: ' + e.message

if __name__ == '__main__':
    unittest.main()