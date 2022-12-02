import copy
from uuid import uuid4


class Order(object):
    def generate_dict(self):
        ret = copy.copy(self.__dict__)
        ret["owner"] = self.owner.get_uuid()
        return ret

    def __init__(self, color, owner, payment_type):
        self.owner = owner
        self.payment_type = payment_type
        self.color = color
        self.uuid = uuid4().hex
        self.progress = {
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
        return self.progress

    def is_complite(self):
        return all(self.progress.values())
