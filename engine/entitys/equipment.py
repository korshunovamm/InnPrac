import copy
import json
from cmath import inf
from uuid import uuid4

from engine.entitys.order import Order

import os
from pathlib import Path


abs_path = os.path.realpath(__file__)
data_abs_path = str(Path(abs_path).parent.parent.parent) + "/data"

def read_file(path: str):
    f = open(path, 'r')
    ret = f.read()
    f.close()
    return ret


# path_to_file = str(Path(abs_path).parent.parent.parent) + "/data/equipments.json"
equData = json.loads(read_file(data_abs_path+"/equipments.json"))


class Equipment(object):
    def generate_dict(self):
        ret = copy.copy(self.__dict__)
        ret['owner'] = self.owner.get_uuid()
        return ret

    def get_color(self):
        return self.color

    def get_price(self):
        return self.price

    def get_repair(self):
        return self.repair

    def get_reagents(self):
        return self.reagents

    def get_type(self):
        return self.type

    def get_expenses(self):
        return self.expenses

    def get_services(self):
        return self.services
    # конструктор
    def __init__(self, owner, eq_type: str, eq_color: str):
        self.max_power = 0
        self.power: int = 0
        self.selled_power: dict[str, int] = {}
        self.reagents = 0
        self.broken = False
        self.owner = owner
        self.uuid: str = uuid4().hex
        self.price: int = equData[eq_type]['price']
        self.expenses: int = equData[eq_type]['expenses']
        self.reputation: int = equData[eq_type]['reputation']
        self.repair: int = equData[eq_type]['repair']
        self.reagent_price: int = equData[eq_type]['reagentPrice']
        self.in_room: bool = False
        self.staff_count: dict = {
            'lab_assistant': 0,
            'doctor': 0
        }
        self.services: dict = {'LIS': False, 'serviceContract': False}
        self.type = eq_type
        self.color = eq_color

    def set_room(self, room):
        self.in_room = True
        self.staff_count: int = room.staff_count

    def remove_room(self):
        self.in_room = False
        self.staff_count = {
            'lab_assistant': 0,
            'doctor': 0
        }

    # оборудование сломано

    def get_service_contract_price(self):
        return round(self.price / 2)

    def can_buy_service_contract(self):
        return not self.services['serviceContract']

    def buy_service_contract(self):
        self.services['serviceContract'] = True
        return True

    def is_broken(self):
        return self.broken

    def break_it(self):
        self.broken = True

    def reset_selled_power(self):
        self.selled_power = []

    def get_repair_price(self):
        if self.services['serviceContract']:
            return 0
        else:
            return self.repair

    def repair_it(self):
        self.broken = False

    # мощность

    def update_max_power(self):
        staff = self.staff_count
        if self.broken or self.in_room is False:
            self.max_power = 0
            return
        match self.type:
            case 'pre_analytic':
                if staff['lab_assistant'] == 1:
                    self.max_power = 2
                elif staff['lab_assistant'] == 2:
                    self.max_power = 4
                elif staff['lab_assistant'] >= 3:
                    self.max_power = 6
                if self.services['LIS'] and staff['lab_assistant'] >= 1:
                    self.max_power = 6
            case 'reporting':
                if staff['lab_assistant'] == 1:
                    self.max_power = 2
                elif staff['lab_assistant'] == 2:
                    self.max_power = 4
                elif staff['lab_assistant'] >= 3:
                    self.max_power = 6
                if self.services['LIS']:
                    self.max_power = inf
            case 'hand':
                if staff['lab_assistant'] >= 1 and staff['doctor'] >= 3:
                    if self.services['LIS']:
                        self.max_power = 2
                    else:
                        self.max_power = 1
                else:
                    self.max_power = 0
            case 'semi_manual':
                if staff['lab_assistant'] >= 2 and staff['doctor'] >= 2:
                    if self.services['LIS']:
                        self.max_power = 3
                    else:
                        self.max_power = 2
                else:
                    self.max_power = 0
            case 'auto':
                if staff['lab_assistant'] >= 3 and staff['doctor'] >= 1:
                    self.max_power = 3
                    if self.services['LIS']:
                        self.max_power += 1
                else:
                    self.max_power = 0

    def get_max_power(self):
        self.update_max_power()
        return self.max_power

    def get_power(self):
        return self.power

    def reagents_to_power(self, correction):
        self.update_max_power()
        self.power_to_reagents()
        if self.max_power + correction >= self.reagents:
            self.power = self.reagents
            self.reagents = 0
        else:
            self.reagents -= self.max_power + correction
            self.power = self.max_power + correction

    def power_to_reagents(self):
        self.reagents += self.power
        self.power = 0

    # купить ЛИС
    def get_lis_price(self):
        if self.type == 'pre_analytic':
            return 5
        elif self.type == 'reporting':
            return 20
        else:
            return 30

    def can_buy_lis(self):
        return not self.services['LIS']

    def buy_lis(self):
        self.services['LIS'] = True

    # купить реагенты

    def get_reagent_price(self):
        return self.reagent_price

    def can_buy_reagents(self, amount):
        self.power_to_reagents()
        self.update_max_power()
        if self.reagents + amount <= self.max_power:
            return True
        else:
            return False

    def buy_reagents(self, amount):
        self.reagents += amount

    # расчет репутации
    def get_reputation(self):
        reputation = self.reputation
        if self.services['LIS']:
            reputation += 3
        if self.services['serviceContract']:
            reputation += 1
        return reputation

    # расчет расходы
    def calc_expenses(self):
        expenses = self.expenses
        if self.services['LIS']:
            if self.type == 'reporting':
                expenses += 5
            else:
                expenses += 1
            expenses += 3
        return expenses

    def use(self, order: Order):
        if isinstance(self.selled_power.get(order.get_owner()), int) and self.selled_power[order.get_owner()] > 0:
            if (self.type == 'pre_analytic' and not order.get_progress()['pre_analytic']) or (
                    self.type == 'reporting' and not order.get_progress()['reporting']) or (
                    self.type in ['hand', 'semi_manual', 'auto'] and (
                    not order.get_progress()['analytic']) and order.get_color() == self.color):
                self.selled_power[order.get_owner()] -= 1
                if self.selled_power[order.get_owner()] <= 0:
                    del self.selled_power[order.get_owner()]
                order.progress[self.type] = True
                if all(order.progress.values()):
                    if order.payment_type == 'post_pay':
                        order.owner.money += 20
                return True
            return False
        elif order.get_owner() == self.owner:
            if self.type in ['pre_analytic', 'reporting'] and order.get_progress().get(self.type) is False:
                self.power -= 1
                order.progress[self.type] = True
                if all(order.progress.values()):
                    if order.payment_type == 'post_pay':
                        order.owner.money += 20
                return True
            elif self.type in ['hand', 'semi_manual', 'auto'] and order.get_progress()['analytic'] is False and \
                    order.get_color() == self.color:
                self.power -= 1
                order.progress['analytic'] = True
                if all(order.progress.values()):
                    if order.payment_type == 'post_pay':
                        order.owner.money += 20
                return True
            return False
        return False

    def sell_power(self, pl_uuid, amount):
        if amount <= self.power:
            self.power -= amount
            if pl_uuid not in self.selled_power:
                self.selled_power[pl_uuid] = 0
            self.selled_power[pl_uuid] += amount
            return True
        else:
            return False

    def can_work(self):

        return not self.broken

    def get_uuid(self) -> str:
        return self.uuid
