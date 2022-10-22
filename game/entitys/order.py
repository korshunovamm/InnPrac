import copy
import json
from uuid import uuid4


class Order(object):
    def generate_dict(self):
        return self.__dict__

    def __init__(self, color, owner_uuid):
        self.owner_uuid = owner_uuid
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
        return self.owner_uuid

    def get_progress(self):
        return self.complite

    def is_complite(self):
        return self.complite['pre_analytic'] and self.complite['analytic'] and self.complite['reporting']
