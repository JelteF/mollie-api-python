from mollie.api.object.base_object import BaseObject


class Method(BaseObject):
    IDEAL = 'ideal'
    PAYSAFECARD = 'paysafecard'
    CREDITCARD = 'creditcard'
    MISTERCASH = 'mistercash'
    BANKTRANSFER = 'banktransfer'
    PAYPAL = 'paypal'
    BITCOIN = 'bitcoin'

    def get_minimum_amount(self):
        if not self['amount'] or 'minimum' not in self['amount']:
            return None
        return float(self['amount']['minimum'])

    def get_maximum_amount(self):
        if not self['amount'] or 'maximum' not in self['amount']:
            return None
        return float(self['amount']['maximum'])

    def get_normal_image(self):
        if not self['image'] or 'normal' not in self['image']:
            return None
        return str(self['image']['normal'])

    def get_bigger_image(self):
        if not self['image'] or 'bigger' not in self['image']:
            return None
        return str(self['image']['bigger'])
