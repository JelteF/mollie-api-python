from mollie.api.object.base_object import BaseObject


class Payment(BaseObject):
    STATUS_OPEN = 'open'
    STATUS_PENDING = 'pending'
    STATUS_CANCELLED = 'cancelled'
    STATUS_EXPIRED = 'expired'
    STATUS_PAID = 'paid'
    STATUS_PAIDOUT = 'paidout'
    STATUS_REFUNDED = 'refunded'

    def is_open(self):
        return self['status'] == self.STATUS_OPEN

    def is_pending(self):
        return self['status'] == self.STATUS_PENDING

    def is_paid(self):
        return 'paidDatetime' in self and self['paidDatetime']

    def get_payment_url(self):
        if 'links' not in self:
            return None
        return self['links']['paymentUrl']


class Refund(BaseObject):

    def is_fully_refunded(self):
        return self.get('amount') == self.get('amountRefunded')