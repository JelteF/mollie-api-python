from mollie.api.object.base_object import BaseObject


class List(BaseObject):
    def __init__(self, result, object_type):
        BaseObject.__init__(self, result)
        self.object_type = object_type

    def __iter__(self):
        for item in self['data']:
            yield self.object_type(item)

    def get_total_count(self):
        if 'totalCount' not in self:
            return None
        return self['totalCount']

    def get_offset(self):
        if 'offset' not in self:
            return None
        return self['offset']

    def get_count(self):
        if 'count' not in self:
            return None
        return self['count']
