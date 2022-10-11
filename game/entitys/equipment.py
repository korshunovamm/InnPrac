import copy
import inspect
import json
from uuid import uuid4

from game.entitys.powerUnit import PowerUnit


def read_file(path: str):
    f = open(path, 'r')
    ret = f.read()
    f.close()
    return ret


equData = json.loads(read_file('data/equipments.json'))


class Equipment(object):

    def generate_dict(self):
        ret = self.__dict__
        for x in ret['power_units']:
            ret['power_units'][x] = ret['power_units'][x].generate_dict()
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

    # конструктор
    def __init__(self, eq_type: str, eq_color: str):
        self.max_power = 0
        self.power_units = {}
        self.reagents = 0
        self.broken = False
        self.uuid: str = uuid4().hex
        self.price: int = equData[eq_type]['price']
        self.expenses: int = equData[eq_type]['expenses']
        self.reputation: int = equData[eq_type]['reputation']
        self.repair: int = equData[eq_type]['repair']
        self.reagentPrice: int = equData[eq_type]['reagentPrice']
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

    # покупка реагентов

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

                if self.services['LIS'] and staff['lab_assistant'] >= 1:
                    self.max_power = 10

            case 'hand':
                if staff['lab_assistant'] >= 1 and staff['doctor'] >= 3:
                    if self.services['LIS']:
                        self.max_power = 2
                    else:
                        self.max_power = 1
            case 'semi_manual':
                if staff['lab_assistant'] >= 2 and staff['doctor'] >= 2:
                    if self.services['LIS']:
                        self.max_power = 3
                    else:
                        self.max_power = 2
            case 'auto':
                if staff['lab_assistant'] >= 3 and staff['doctor'] >= 1:
                    if self.services['LIS']:
                        self.max_power = 4
                    else:
                        self.max_power = 3
            # заказы

    def get_max_power(self):
        self.update_max_power()
        return self.max_power

    def get_power_units(self):
        self.reagents_to_units()
        return self.power_units

    def reagents_to_units(self):
        self.update_max_power()
        self.units_to_reagents()
        if self.can_work():
            for x in range(self.reagents):
                eq_type = self.type
                if eq_type == 'hand' or eq_type == 'semi_manual' or eq_type == 'auto':
                    eq_type = 'analytic'
                unit = PowerUnit(eq_type, self.color)
                self.power_units[unit.get_uuid()] = unit
                self.reagents -= 1

    def units_to_reagents(self):
        reagents = self.reagents
        for x in self.power_units:
            if self.power_units[x].is_used() is False:
                reagents += 1
        self.power_units = {}
        self.reagents = reagents

    # купить ЛИС
    def get_lis_price(self):
        if self.type == 'pre_analytic':
            return 5
        elif self.type == 'reporting':
            return 20
        else:
            return 30

    def can_buy_lis(self):
        if self.services['LIS']:
            return False
        else:
            return True

    def buy_lis(self):
        self.services['LIS'] = True
        self.update_max_power()

    # купить реагенты

    def get_reagent_price(self):
        return self.reagentPrice

    def can_buy_reagents(self, amount):
        self.units_to_reagents()
        self.update_max_power()
        if self.reagents + amount <= self.max_power:
            return True
        else:
            return False

    def buy_reagents(self, amount):
        self.reagents += amount

    # расчет репутации
    def calc_reputation(self):
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

    # переход от первой стадии к второй
    def next_stage(self):
        self.reagents_to_units()

    def can_work(self):
        if self.broken:
            return False
        else:
            return True

    def get_uuid(self) -> str:
        return self.uuid
