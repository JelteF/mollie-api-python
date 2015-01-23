from mollie.api.error import *
from mollie.api.object.payment import Payment, Refund
from .base_resource import BaseResource


class Payments(BaseResource):
    RESOURCE_ID_PREFIX = 'tr_'

    def get_resource_object(self, result):
        return Payment(result)

    def get(self, payment_id):
        if not payment_id or self.RESOURCE_ID_PREFIX not in payment_id:
            raise Error(
                'Invalid payment ID: "%s". A payment ID should start with "%s".' % (payment_id, self.RESOURCE_ID_PREFIX)
            )
        return super(Payments, self).get(payment_id)

    def refund(self, payment):
        return self.client.payment_refunds.on(payment).create()


class Refunds(BaseResource):
    payment_id = None

    def get_resource_object(self, result):
        return Refund(result)

    def get_resource_name(self):
        return 'payments/%i/refunds' % self.payment_id

    def on(self, payment):
        self.payment_id = payment['id']
        return self