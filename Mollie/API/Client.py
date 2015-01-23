import os
import sys
import ssl
import re
import pkg_resources

import requests

from mollie.api.resource.payments import Payments, Refunds
from mollie.api.resource.issuers import Issuers
from mollie.api.resource.methods import Methods
from mollie.api.error import Error
from mollie.api import API_ENDPOINT, API_VERSION, CLIENT_VERSION

class Client:

    def __init__(self):
        self.api_endpoint = API_ENDPOINT
        self.api_version = API_VERSION
        self.api_key = ''
        self.payments = Payments(self)
        self.payment_refunds = Refunds(self)
        self.issuers = Issuers(self)
        self.methods = Methods(self)
        self.version_strings = []
        self.add_version_string('mollie/' + CLIENT_VERSION)
        self.add_version_string('Python/' + sys.version.split(' ')[0])
        self.add_version_string('OpenSSL/' + ssl.OPENSSL_VERSION.split(' ')[1])

    def get_api_endpoint(self):
        return self.api_endpoint

    def set_api_endpoint(self, api_endpoint):
        self.api_endpoint = api_endpoint.strip().rstrip('/')

    def set_api_key(self, api_key):
        api_key = api_key.strip()
        if not re.compile('^(live|test)_\w+$').match(api_key):
            raise Error('Invalid API key: "%s". An API key must start with "test_" or "live_".' % api_key)
        self.api_key = api_key

    def add_version_string(self, version_string):
        self.version_strings.append(version_string.replace(r'\s+', '-'))

    def get_ca_cert(self):
        cacert = pkg_resources.resource_filename('mollie.api', 'cacert.pem')
        if not cacert or len(cacert) < 1:
            raise Error('Unable to load cacert.pem')
        return cacert

    def perform_http_call(self, http_method, path, data=None, params=None):
        if not self.api_key:
            raise Error('You have not set an API key. Please use set_api_key() to set the API key.')
        url = self.api_endpoint + '/' + self.api_version + '/' + path
        user_agent = ' '.join(self.version_strings)
        uname = ' '.join(os.uname())
        try:
            response = requests.request(
                http_method, url,
                verify=self.get_ca_cert(),
                headers={
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + self.api_key,
                    'User-Agent': user_agent,
                    'X-mollie-Client-Info': uname
                },
                params=params,
                data=data
            )
        except Exception as e:
            raise Error('Unable to communicate with mollie: %s.' % str(e))
        return response