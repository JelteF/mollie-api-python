from mollie.api.resource.base_resource import BaseResource
from mollie.api.object.issuer import Issuer


class Issuers(BaseResource):
    def get_resource_object(self, result):
        return Issuer(result)