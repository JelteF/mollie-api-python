# coding=utf-8
#
# Example 5 - How to retrieve your payments history.
#
import sys
import os
from mollie.api.client import Client
from mollie.api.error import Error
from app import EXAMPLE_API_KEY
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
        mollie = Client()
        mollie.set_api_key(EXAMPLE_API_KEY)

        #
        # Get the all payments for this API key ordered by newest.
        #
        payments = mollie.payments.all()

        body = 'Your API key has %u payments, last %u:<br>' % (payments['totalCount'], payments['count'])

        for payment in payments:
            body += "&euro; %s, status: '%s'<br>" % (payment['amount'], payment['status'])

        return body

    except Error as e:
        return 'API call failed: ' + e.message

# if __name__ == '__main__':
#     print main()
