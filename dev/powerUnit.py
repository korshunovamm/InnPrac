import copy
from uuid import uuid4


class PowerUnit(object):
    def generate_dict(self):
        return copy.copy(self.__dict__)

    def get_uuid(self):
        return self.uuid

    def __init__(self, eq_type: str, color: str):
        self.used: bool = False
        self.type = eq_type
        self.checkColor: bool = False
        if eq_type == 'analytic':
            self.color = color
            self.checkColor = True
        self.uuid = uuid4().hex

    def use(self, order):
        if not self.used:
            if (not order.progress[self.type]) and (not self.checkColor) or self.color == order.color:
                order.progress[self.type] = True
                return True
            else:
                return False
        else:
            return False

    def is_used(self):
        return self.used
