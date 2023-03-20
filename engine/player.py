import copy
import json
import random
from uuid import uuid4
import os

from engine.entitys.equipment import Equipment
from engine.entitys.order import Order
from engine.entitys.room import Room
from pathlib import Path


abs_path = os.path.realpath(__file__)
data_abs_path = str(Path(abs_path).parent.parent) + "/data"


def read_file(path: str):
    f = open(path, 'r')
    ret = f.read()
    f.close()
    return ret


class Player:
    def generate_dict(self):
        ret = copy.copy(self.__dict__)
        ret['orders'] = {}
        for x in self.orders:
            ret['orders'][x] = self.orders[x].generate_dict()
        ret['rooms'] = {}
        for x in self.rooms:
            ret['rooms'][x] = self.rooms[x].generate_dict()
        ret['equipments'] = {}
        for x in self.equipments:
            ret['equipments'][x] = self.equipments[x].generate_dict()
        ret['trade_requests'] = {}
        for x in self.trade_requests:
            ret['trade_requests'][x] = self.trade_requests[x].generate_dict()
        ret['pledge_requests'] = {}
        for x in self.pledge_requests:
            ret['pledge_requests'][x] = self.pledge_requests[x].generate_dict()
        ret['bank_pledges'] = {}
        for x in self.bank_pledges:
            ret['bank_pledges'][x] = self.bank_pledges[x].generate_dict()
        ret['power_sells'] = {}
        for x in self.power_sells:
            ret['power_sells'][x] = self.power_sells[x].generate_dict()
        if self.last_event is not None:
            ret['last_event'] = self.last_event.generate_dict()
        return ret

    # конструктор
    def __init__(self, name: str):
        # динамичные параметры игрока
        self.last_event = None
        self.pay_type: str = 'post_pay'
        self.power_sells: dict = {}  # сбрасывать каждый месяц
        self.my_power: list[dict[str, str or int]] = []  # сбрасывать каждый месяц
        self.reputation = 0  # репутация
        self.events: dict[str, bool] = {  # события, сбрасывать динамичные
            'saved_from_negative_analytics': False,
            'power_is_calculated': False,
            'power_reduction': False,  # снижение мощности
            'need_have_logistic': False,  # нужна ли логистика для выполнения чужих заказов или своих на чужих мощностях
        }
        self.name = name
        self.base_reputation = 0  # базовая репутация игрока
        self.equipments: dict = {}
        self.services: dict[str, bool] = {
            'logistic': False,
            'training': False
        }
        self.pledge_requests = {}
        self.bank_pledges = {}
        self.trade_requests = {}
        self.promotion: int = 0  # сбрасывать каждый месяц
        self.rooms: dict[str, Room] = {}
        self.orders_input: dict = {
            'yellow': False,
            'red': False,
            'blue': False,
            'green': False,
            'purple': False,
            'grey': False
        }  # сбрасывать каждый месяц
        self.orders_correction: dict = {
            'yellow': 0,
            'red': 0,
            'blue': 0,
            'green': 0,
            'purple': 0,
            'grey': 0
        }  # сбрасывать каждый месяц
        self.orders_is_calculated = False  # сбрасывать каждый месяц
        self.money: int = 120
        self.credit: int = 0
        self.uuid = uuid4().hex
        self.equipments_rooms: dict[str, str] = {}
        self.orders: dict[str, Order] = {}  # сбрасывать каждый месяц
        self.temp_reputation = 0  # сбрасывать каждый месяц

    # имена, uuid и пароль

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_uuid(self):
        return self.uuid

    def get_money(self):
        return self.money

    def set_payment_type(self, pay_type):
        self.pay_type = pay_type

    def buy_ad(self, count):
        if self.buy(count):
            self.promotion += count
            return True
        return False

    def get_credit(self):
        return self.credit

    # покупка
    def buy(self, price: int, credit: bool = False):
        if credit:
            self.credit += int(round(price * 1.5, 0))
            return True
        self.money -= price

    # продажа
    def sell(self, price: int):
        self.money += int(price)

    # Заказы лаборатории
    def get_orders_input(self):
        return self.orders_input

    @staticmethod
    def order_level_to_amount(order_level: int):
        lev: list = [
            [0], [0, 0, 0, 1, 2], [0, 0, 1, 2, 3], [0, 1, 2, 3, 4], [1, 2, 3, 4, 4]
        ]
        return random.choice(lev[order_level])

    def orders_refund(self):
        if self.pay_type == 'pre_pay':
            for order_name in self.orders:
                if not self.orders[order_name].is_complite():
                    self.money -= 30

    def calc_orders_reputation(self):
        orders_count = len(self.orders)
        complete_orders_count = 0
        for x in self.orders:
            if self.orders[x].is_complite():
                complete_orders_count += 1
        if orders_count != 0:
            orders_reputation = complete_orders_count / orders_count
            if complete_orders_count == 0:
                self.base_reputation -= 5
            elif orders_reputation == 1:
                self.base_reputation += 5
            elif orders_reputation >= 0.5:
                self.base_reputation += 3
            else:
                self.base_reputation -= 3

    def calc_reputation(self):
        rep: int = self.promotion + self.temp_reputation + self.base_reputation
        if self.services['logistic']:
            rep += 1
        if self.services['training']:
            rep += 1
        for ro in self.rooms.values():
            rep += ro.get_reputation()
        for eq in self.equipments.values():
            rep += eq.get_reputation()
        self.reputation = rep
        return rep

    def set_orders_input(self, orders_input):
        self.orders_input = orders_input

    def calc_orders_count(self, orders_level):
        if self.orders_is_calculated:
            return self.get_orders()
        self.orders_is_calculated = True
        self.orders = {}
        for order_color in self.orders_input:
            if self.orders_input[order_color]:
                orders_count = self.order_level_to_amount(orders_level) + self.orders_correction[order_color]
                for _ in range(orders_count):
                    order = Order(order_color, self, self.pay_type)
                    self.orders[order.get_uuid()] = order
        return self.get_orders()

    def get_orders(self):
        return self.orders

    def buy_logistic_service(self):
        if self.money >= 5 and not self.services['logistic']:
            self.buy(5)
            self.services['logistic'] = True
            return True
        return False

    def buy_training_service(self):
        if self.money >= 5 and not self.services['training']:
            self.buy(5)
            self.services['training'] = True
            return True
        return False

    # помещения лаборатории
    def can_buy_room(self):
        return self.money >= Room.get_price()

    def buy_room(self):
        ro = Room()
        self.buy(ro.get_price())
        self.rooms[ro.get_uuid()] = ro
        return ro

    def get_rooms(self):
        return self.rooms

    def get_room(self, uuid):
        return self.rooms.get(uuid)

    def sell_room(self, room_uuid) -> bool:
        if room_uuid in self.rooms:
            self.sell(round(self.rooms[room_uuid].get_price() / 2, 0))
            eq = self.rooms[room_uuid].get_equipment()
            if eq is not None:
                self.move_equipment_from_room(eq.get_uuid())
                del self.rooms[room_uuid]
                return True
            else:
                del self.rooms[room_uuid]
                return True
        else:
            return False

    # оборудование комнат
    def can_buy_equipment(self, equipment_info):
        return self.money >= equipment_info['price']

    def buy_equipment(self, eq_type: str, eq_color: str):
        eq = Equipment(self, eq_type, eq_color)
        self.equipments[eq.get_uuid()] = eq
        return eq

    def sell_equipment(self, eq_uuid: str):
        if eq_uuid in self.equipments:
            eq = self.equipments[eq_uuid]
            if eq.is_broken():
                self.sell(round(eq.get_price() / 10, 0))
            else:
                self.sell(round(eq.get_price() / 2, 0))
            del self.equipments[eq_uuid]
            return True, eq.get_type(), eq.get_color()
        elif eq_uuid in self.equipments_rooms:
            eq = self.rooms[self.equipments_rooms[eq_uuid]].get_equipment()
            if eq.is_broken():
                self.sell(round(eq.get_price() / 10, 0))
            else:
                self.sell(round(eq.get_price() / 2, 0))
            self.rooms[self.equipments_rooms[eq_uuid]].set_equipment(None)
            del self.equipments_rooms[eq_uuid]
            return True, eq.get_type(), eq.get_color()
        else:
            return False

    def move_equipment_to_room(self, eq_uuid: str, ro_uuid: str):
        if eq_uuid in self.equipments and self.rooms[ro_uuid].get_equipment() is None:
            self.equipments[eq_uuid].set_room(self.rooms[ro_uuid])
            self.rooms[ro_uuid].set_equipment(self.equipments[eq_uuid])
            self.equipments_rooms[eq_uuid] = ro_uuid
            del self.equipments[eq_uuid]
            return True
        else:
            return False

    def move_equipment_from_room(self, ro_uuid: str):
        ro = self.rooms[ro_uuid]
        eq = ro.get_equipment()
        if eq is not None:
            ro.set_equipment(None)
            self.equipments[eq.get_uuid()] = eq
            eq.remove_room()
            del self.equipments_rooms[eq.get_uuid()]
            return True
        else:
            return False

    def can_upgrade_equipment(self, eq_uuid: str, eq_new_type: str):
        equipment_data = json.loads(read_file('data/equipments.json'))
        equipment_prices = {
            "hand": equipment_data['hand']['price'],
            "semi_manual": equipment_data['semi_manual']['price'],
            "auto": equipment_data['auto']['price']
        }
        if eq_uuid in self.equipments:
            eq: Equipment = self.equipments[eq_uuid]
        elif eq_uuid in self.equipments_rooms:
            eq: Equipment = self.rooms[self.equipments_rooms[eq_uuid]].get_equipment()
        else:
            return False
        if eq.get_type() not in ["hand", "semi_manual"] or eq_new_type not in ["semi_manual", "auto"]:
            return False
        eq_price = equipment_prices[eq.get_type()]
        eq_new_price = equipment_prices[eq_new_type]
        upgrade_price = eq_new_price - eq_price
        return self.money >= upgrade_price

    def upgrade_equipment(self, eq_uuid: str, eq_new_type: str):
        if not self.can_upgrade_equipment(eq_uuid, eq_new_type):
            return False, None
        equipment_data = json.loads(read_file('data/equipments.json'))
        equipment_prices = {
            "hand": equipment_data['hand']['price'],
            "semi_manual": equipment_data['semi_manual']['price'],
            "auto": equipment_data['auto']['price']
        }
        eq = self.get_equipment(eq_uuid)
        eq_price = equipment_prices[eq.get_type()]
        eq_new_price = equipment_prices[eq_new_type]
        upgrade_price = eq_new_price - eq_price
        self.buy(upgrade_price)
        new_eq: Equipment = Equipment(self, eq_new_type, eq.get_color())
        if eq.in_room:
            ro_uuid = self.equipments_rooms[eq_uuid]
            ro = self.rooms[ro_uuid]
            new_eq.set_room(ro)
            self.equipments_rooms[new_eq.get_uuid()] = ro_uuid
            ro.set_equipment(new_eq)
        else:
            self.equipments[new_eq.get_uuid()] = new_eq
        if eq.is_broken():
            new_eq.break_it()
        new_eq.services = eq.get_services()
        new_eq.buy_reagents(eq.get_reagents())
        new_eq.update_max_power()
        return True, new_eq

    def get_equipment(self, eq_uuid: str):
        if eq_uuid in self.equipments:
            return self.equipments[eq_uuid]
        elif eq_uuid in self.equipments_rooms:
            return self.rooms[self.equipments_rooms[eq_uuid]].get_equipment()
        else:
            return None

    def buy_service_contract(self, eq_uuid: str):
        eq = self.get_equipment(eq_uuid)
        if eq is not None:
            if eq.get_service_contract_price() < self.money and eq.can_buy_service_contract():
                self.buy(eq.buy_service_contract())
                return True, eq
            return False, None
        return False, None

    def buy_service_maintenance(self, eq_uuid):
        eq = self.get_equipment(eq_uuid)
        if eq is not None:
            if eq.get_repair_price() < self.money and eq.is_broken():
                eq.repair_it()
                self.buy(eq.get_repair_price())
                return True, eq
            return False, None
        return False, None

    def can_buy_lis(self, eq_uuid: str):
        eq = self.get_equipment(eq_uuid)
        if eq is not None and eq.get_lis_price() < self.money and eq.can_buy_lis():
            return True
        return False

    def repair_equipment(self, eq_uuid: str):
        eq = self.get_equipment(eq_uuid)
        if eq['state'] == 'broken' and self.money >= eq.get_repair_price():
            self.buy(eq.get_repair_price())
            eq.repair_it()
            return True
        return True

    # купить персонал
    def buy_staff(self, ro_uuid: str, staff_type: str, amount: int):
        ro = self.get_room(ro_uuid)
        staff_info = json.loads(read_file(data_abs_path + "/staff.json"))[staff_type]
        if self.money >= staff_info['price'] and \
                ro.get_staff()[staff_type] < ro.get_max_staff()[staff_type]:
            self.buy(staff_info['price'])
            return ro.add_staff(staff_type, amount)
        else:
            return False

    #  перемещать персонал
    def move_staff(self, ro_uuid_from: str, ro_uuid_to, staff_type: str):
        ro_from = self.rooms[ro_uuid_from]
        ro_to = self.rooms[ro_uuid_to]
        if ro_from.get_staff()[staff_type] > 0 and \
                ro_to.get_staff()[staff_type] < ro_to.get_max_staff()[staff_type]:
            ro_from.remove_staff(staff_type)
            ro_to.add_staff(staff_type, 1)
            return True
        else:
            return False

    # купить реагенты

    def buy_reagents(self, eq_uuid: str, amount: int):
        eq = self.get_equipment(eq_uuid)
        if eq is not None and self.money >= eq.get_reagent_price() * amount:
            if eq.can_buy_reagents(amount):
                eq.buy_reagents(amount)
                self.buy(eq.get_reagent_price() * amount)
                return True
            return False
        return False

    # каждый месяц

    def calc_expenses(self):
        exp = 0
        if self.services['logistic']:
            exp += 1
        if self.services['training']:
            exp += 1
        for ro in self.rooms.values():
            exp += ro.get_expenses()
        for eq in self.equipments.values():
            exp += eq.get_expenses()
        return exp

    def calc_power(self):
        if not self.events['power_is_calculated']:
            for ro in self.rooms.values():
                eq = ro.get_equipment()
                if eq is not None:
                    eq.reagents_to_power(-int(self.events['power_reduction']))

    def get_trade_req(self):
        return self.trade_requests

    def add_trade_req(self, trade_request):
        self.trade_requests[trade_request.get_uuid()] = trade_request

    def dump_params(self):
        self.temp_reputation = 0
        self.orders = {}
        self.orders_correction = {
            'yellow': 0,
            'red': 0,
            'blue': 0,
            'green': 0,
            'purple': 0,
            'grey': 0
        }
        self.promotion = 0
        self.orders_is_calculated = False
        self.orders_input = {
            'yellow': False,
            'red': False,
            'blue': False,
            'green': False,
            'purple': False,
            'grey': False
        }
        self.events = {
            'saved_from_negative_analytics': self.events['saved_from_negative_analytics'],
            'power_is_calculated': False,
            'power_reduction': False,  # снижение мощности
            'need_have_logistic': False,  # нужна ли логистика для выполнения чужих заказов или своих на чужих мощностях
        }
        self.power_sells = {}
        self.my_power = []
