import copy
import inspect
import json
from uuid import uuid4

from game.entitys.equipment import Equipment


class Room:
    def generate_dict(self):
        ret = copy.copy(self.__dict__)
        if self.equipment is not None:
            ret['equipment'] = self.equipment.generate_dict()
        return ret

    def __init__(self):
        self.uuid = uuid4().hex
        self.equipment: Equipment = None
        self.in_trade = False
        self.staff_count = {
            'doctor': 0,
            'lab_assistant': 0
        }

    # статические параметры комнаты
    @staticmethod
    def get_price():
        return 10

    @staticmethod
    def get_base_expenses():
        return 3

    @staticmethod
    def get_base_reputation():
        return 1

    @staticmethod
    def get_max_staff():
        return {
            'doctor': 4,
            'lab_assistant': 4
        }

    def get_uuid(self):
        return self.uuid

    # оборудование

    def can_buy_equipment(self):
        return self.equipment is None

    def get_equipment(self):
        return self.equipment

    def set_equipment(self, equipment: Equipment | None):
        self.equipment = equipment

    # врачи и лаборанты

    def get_staff(self):
        return self.staff_count

    def add_staff(self, ro_type):
        if self.staff_count[ro_type] < 4:
            self.staff_count[ro_type] += 1
            if self.equipment is not None:
                self.equipment.update_max_power()
            return True
        else:
            return False

    def remove_staff(self, staff_type):
        if self.staff_count[staff_type] > 0:
            self.staff_count[staff_type] -= 1
            return True

    # показатели комнаты вместе с оборудованием
    def get_reputation(self):
        ret: int = self.get_base_reputation()
        if self.equipment is not None:
            ret += self.equipment.get_reputation()
        ret += self.staff_count['doctor'] + self.staff_count['lab_assistant']
        return ret

    def get_expenses(self):
        ret: int = self.get_base_expenses()
        # если оборудование есть, то добавляем его расходы
        ret += self.staff_count['doctor'] * 2 + self.staff_count['lab_assistant']
        if self.equipment is not None:
            ret += self.equipment.get_expenses()
        return ret
