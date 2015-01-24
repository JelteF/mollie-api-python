from mollie.api import HTTP_DELETE, HTTP_GET, HTTP_POST
from mollie.api.error import Error
import json


class BaseResource():
    REST_CREATE = HTTP_POST
    REST_UPDATE = HTTP_POST
    REST_READ = HTTP_GET
    REST_LIST = HTTP_GET
    REST_DELETE = HTTP_DELETE
    DEFAULT_LIMIT = 10

    def __init__(self, client):
        self.client = client

    def get_resource_object(self, result):
        raise NotImplementedError()

    def get_resource_name(self):
        return self.__class__.__name__.lower()

    def rest_create(self, data, params=None):
        path = self.get_resource_name()
        result = self.perform_api_call(self.REST_CREATE, path, data, params)
        return self.get_resource_object(result)

    def rest_read(self, resource_id, params=None):
        path = self.get_resource_name() + '/' + str(resource_id)
        result = self.perform_api_call(self.REST_READ, path, None, params)
        return self.get_resource_object(result)

    def rest_update(self, resource_id, data, params=None):
        path = self.get_resource_name() + '/' + str(resource_id)
        result = self.perform_api_call(self.REST_UPDATE, path, data, params)
        return self.get_resource_object(result)

    def rest_delete(self, resource_id, params=None):
        path = self.get_resource_name() + '/' + str(resource_id)
        return self.perform_api_call(self.REST_DELETE, path, None, params)

    def rest_list(self, params=None):
        path = self.get_resource_name()
        result = self.perform_api_call(self.REST_LIST, path, None, params)
        return result, self.get_resource_object({}).__class__

    def create(self, data=None):
        try:
            if data is not None:
                data = json.dumps(data)
        except Exception as e:
            raise Error('Error encoding parameters into JSON: "%s"' % str(e))
        return self.rest_create(data)

    def get(self, resource_id):
        return self.rest_read(resource_id)

    def update(self, resource_id, data):
        try:
            data = json.dumps(data)
        except Exception as e:
            raise Error('Error encoding parameters into JSON: "%s"' % str(e))
        return self.rest_update(resource_id, data)

    def delete(self, resource_id):
        return self.rest_delete(resource_id)

    def all(self, offset=0, count=DEFAULT_LIMIT):
        return self.rest_list({
            'offset': offset,
            'count': count
        })

    def perform_api_call(self, http_method, path, data=None, params=None):
        body = self.client.perform_http_call(http_method, path, data, params)
        try:
            result = body.json()
        except Exception as e:
            raise Error('Unable to decode mollie response: "%s".' % body)
        if 'error' in result:
            error = Error('Error executing API call (%s): %s.' % (result['error']['type'], result['error']['message']))
            if 'field' in result['error']:
                error.field = result['error']['field']
            raise error
        return result
