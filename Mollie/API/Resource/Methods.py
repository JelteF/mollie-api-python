from mollie.api.resource.base_resource import BaseResource
from mollie.api.object.method import Method


class Methods(BaseResource):
    def get_resource_object(self, result):
        return Method(result)