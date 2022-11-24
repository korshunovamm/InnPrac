import copy
import json
from uuid import uuid4


class Order(object):
    def generate_dict(self):
        ret = copy.copy(self.__dict__)
        ret["owner"] = self.owner.get_uuid()
        return ret

    def __init__(self, color, owner):
        self.owner = owner
        self.color = color
        self.uuid = uuid4().hex
        self.complite = {
            'pre_analytic': False,
            'analytic': False,
            'reporting': False
        }

    def get_uuid(self):
        return self.uuid

    def get_color(self):
        return self.color

    def get_owner(self):
        return self.owner

    def get_progress(self):
        return self.complite

    def is_complite(self):
        return self.complite['pre_analytic'] and self.complite['analytic'] and self.complite['reporting']
