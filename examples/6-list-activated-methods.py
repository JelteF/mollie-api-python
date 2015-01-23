# coding=utf-8
#
#  Example 6 - How to get the currently activated payment methods.
#
import sys, os

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
        # See: https://www.mollie.nl/beheer/account/profielen/
        #
        mollie = mollie.API.Client()
        mollie.set_api_key('test_bt7vvByF6jTcBR4dLuW66eNnHYNIJp')

        #
        # Get the all the activated methods for this API key.
        #
        methods = mollie.methods.all()

        body = 'Your API key has %u activated payment methods:<br>' % int(methods['totalCount'])

        for method in methods:
            body += '<div style="line-height:40px; vertical-align:top">'
            body += '<img src="%s"> %s (%s)' % (method['image']['normal'], method['description'], method['id'])
            body += '</div>'

        return body

    except mollie.API.Error as e:
        return 'API call failed: ' + e.message

if __name__ == '__main__':
    print main()
