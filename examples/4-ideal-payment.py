# coding=utf-8
#
# Example 4 - How to prepare an iDEAL payment with the mollie API.
#
import sys
import os
import time
import flask
from app import database_write, EXAMPLE_API_KEY
from mollie.api.client import Client
from mollie.api.object.method import Method
from mollie.api.error import Error
#
# Add mollie library to module path so we can import it.
# This is not necessary if you use pip or easy_install.
#
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))


def main ():
    try:
        #
        # Initialize the mollie API library with your API key.
        #
        # See: https://www.lib.nl/beheer/account/profielen/
        #
        mollie = Client()
        mollie.set_api_key(EXAMPLE_API_KEY)

        #
        # First, let the customer pick the bank in a simple HTML form. This step is actually optional.
        #
        if 'issuer' not in flask.request.form:
            body = '<form method="post">Select your bank: <select name="issuer">'

            for issuer in mollie.issuers.all():
                if issuer['method'] == Method.IDEAL:
                    body += '<option value="%s">%s</option>' % (issuer['id'], issuer['name'])

            body += '<option value="">or select later</option>'
            body += '</select><button>OK</button></form>'
            return body

        else:
            #
            # Get the posted issuer id.
            #
            issuer_id = None

            if flask.request.form['issuer']:
                issuer_id = str(flask.request.form['issuer'])

            #
            # Generate a unique order number for this example. It is important to include this unique attribute
            # in the redirectUrl (below) so a proper return page can be shown to the customer.
            #
            order_nr = int(time.time())

            #
            # Payment parameters:
            # amount        Amount in EUROs. This example creates a € 10,- payment.
            # description   Description of the payment.
            # redirectUrl   Redirect location. The customer will be redirected there after the payment.
            # metadata      Custom metadata that is stored with the payment.
            # method        Payment method "ideal".
            # issuer        The customer's bank. If empty the customer can select it later.
            #
            payment = mollie.payments.create({
                'amount': 10.00,
                'description': 'My first API payment',
                'redirectUrl': flask.request.url_root + '3-return-page?order_nr=' + str(order_nr),
                'metadata': {
                    'order_nr': order_nr
                },
                'method': 'ideal',
                'issuer': issuer_id
            })

            #
            # In this example we store the order with its payment status in a database.
            #
            database_write(order_nr, payment['status'])

            #
            # Send the customer off to complete the payment.
            #
            return flask.redirect(payment.get_payment_url())

    except Error as e:
        return 'API call failed: ' + e.message


# if __name__ == '__main__':
#     print main()
