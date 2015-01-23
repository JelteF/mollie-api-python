#
# Example 2 - How to verify mollie API Payments in a webhook.
#
import sys
import os
import flask
from app import *
from mollie.api import client
from mollie.api.error import Error
#
# Add mollie library to module path so we can import it.
# This is not necessary if you use pip or easy_install.
#
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))

import mollie


def main():
    try:
        #
        # Initialize the mollie API library with your API key.
        #
        # See: https://www.lib.nl/beheer/account/profielen/
        #
        mollie = client.Client()
        mollie.set_api_key(EXAMPLE_API_KEY)

        #
        # Retrieve the payment's current state.
        #
        if 'id' not in flask.request.form:
            flask.abort(404, 'Unknown payment id')

        payment_id = flask.request.form['id']
        payment = mollie.payments.get(payment_id)
        order_nr = payment['metadata']['order_nr']

        #
        # Update the order in the database.
        #
        database_write(order_nr, payment['status'])

        if payment.is_paid():
            #
            # At this point you'd probably want to start the process of delivering the product to the customer.
            #
            return 'Paid'
        elif payment.is_pending():
            #
            # The payment has started but is not complete yet.
            #
            return 'Pending'
        elif payment.is_open():
            #
            # The payment has not started yet. Wait for it.
            #
            return 'Open'
        else:
            #
            # The payment isn't paid, pending nor open. We can assume it was aborted.
            #
            return 'Cancelled'

    except Error as e:
        return 'API call failed: ' + e.message
#
# if __name__ == '__main__':
#     print main()