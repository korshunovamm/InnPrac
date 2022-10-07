import json
import random
from hashlib import sha256
from uuid import uuid4

from game.entitys.equipment import Equipment
from game.entitys.order import Order
from game.entitys.room import Room


def read_file(path: str):
    f = open(path, 'r')
    ret = f.read()
    f.close()
    return ret


class Player(object):

    # конструктор
    def __init__(self, nickname: str, password: str):
        # динамичные параметры игрока
        self.events = {  # события, TODO: сбрасывать динамичные
            "saved_from_negative_analytics": False,
            "orders_is_calculated": False,
            "power_is_calculated": False,
            "power_reduction": False,  # снижение мощности
            "need_have_logistic": False  # нужна ли логистика для выполнения чужих заказов или своих на чужих мощностях
        }
        self.equipments: dict = {}
        self.services = {
            "logistic": False,
            "training": False
        }
        self.pledges = {

        }
        self.trade_requests = {}
        self.dataIsReady = False  # TODO: сбрасывать каждый месяц
        self.promotion: int = 0  # TODO: сбрасывать каждый месяц
        self.rooms: dict = {}
        self.orders_input: dict = {
            "yellow": False,
            "red": False,
            "blue": False,
            "green": False,
            "purple": False,
            "grey": False
        }
        self.orders_correction: dict = {
            "yellow": 0,
            "red": 0,
            "blue": 0,
            "green": 0,
            "purple": 0,
            "grey": 0
        }  # TODO: сбрасывать каждый месяц
        self.orders_is_calculated = False  # TODO: сбрасывать каждый месяц
        self.money: int = 120
        self.credit: int = 0
        self.nickname = nickname
        self.hash = sha256(password.encode('utf-8')).hexdigest()
        self.uuid = uuid4().hex
        self.equipments_rooms = {}
        self.orders = {}
        self.orders_reputation = 0

    # имена, uuid и пароль
    def get_uuid(self):
        return self.uuid

    def get_nickname(self):
        return self.nickname

    def get_hash(self):
        return self.hash

    def get_money(self):
        return self.money

    def set_ads_params(self, params):
        self.promotion = params
        self.dataIsReady = True

    def get_ads_params(self):
        return self.promotion

    def get_credit(self):
        return self.credit

    def data_is_ready(self):
        return self.dataIsReady

    # покупка
    def buy(self, price: int, credit: bool = False):
        if credit:
            self.credit += int(round(price * 1.5, 0))
            return True
        else:
            if self.money >= price:
                self.money -= price
                return True
            else:
                return False

    # продажа
    def sell(self, price: int):
        self.money += int(price)

    # Заказы лаборатории
    def get_orders_input(self):
        return self.orders_input

    @staticmethod
    def order_level_to_amount(order_level: str):
        lev: dict = {
            1: [0, 0, 0, 1, 2],
            2: [0, 0, 1, 2, 3],
            3: [0, 1, 2, 3, 4],
            4: [1, 2, 3, 4, 4]
        }
        return random.choice(lev[order_level])

    def calc_orders_reputation(self):
        orders_count = len(self.orders)
        complete_orders_count = 0
        for x in self.orders:
            if self.orders[x].is_complite():
                complete_orders_count += 1
        if orders_count == 0:
            self.orders_reputation = 0
        else:
            orders_reputation = complete_orders_count / orders_count
            if complete_orders_count == 0:
                self.orders_reputation = -5
            elif orders_reputation == 1:
                self.orders_reputation = 5
            elif orders_reputation >= 0.5:
                self.orders_reputation = 3
            else:
                self.orders_reputation = -3

    def calc_reputation(self):
        ret: int = self.promotion + self.orders_reputation
        if self.services["logistic"]:
            ret += 1
        if self.services["training"]:
            ret += 1
        for ro in self.rooms.values():
            ret += ro.get_reputation()
        for eq in self.rooms.values():
            ret += eq.get_reputation()
        return ret

    def set_orders_input(self, orders_input):
        self.orders_input = orders_input

    def calc_orders_count(self, orders_level):
        self.orders = {}
        for x in self.orders_input:
            if self.orders_input[x]:
                orders = self.order_level_to_amount(orders_level) + self.orders_correction[x]
                for z in range(orders):
                    order = Order(x, self.uuid)
                    self.orders[order.get_uuid()] = order
        return self.orders

    def get_orders(self):
        return self.orders

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
        return self.money >= equipment_info["price"]

    def buy_equipment(self, eq_type: str, eq_color: str) -> object:
        eq = Equipment(eq_type, eq_color)
        self.equipments[eq.get_uuid()] = eq
        return eq

    def sell_equipment(self, eq_uuid: str):
        self.sell(round(self.equipments[eq_uuid].get_price() / 2, 0))
        if eq_uuid in self.equipments:
            eq = self.equipments[eq_uuid]
            del self.equipments[eq_uuid]
        else:
            eq = self.rooms[self.equipments_rooms[eq_uuid]].get_equipment()
            self.rooms[self.equipments_rooms[eq_uuid]].set_equipment(None)
            del self.equipments_rooms[eq_uuid]
        return eq.get_type(), eq.get_color()

    def move_equipment_to_room(self, eq_uuid: str, ro_uuid: str):
        if eq_uuid in self.equipments.keys() and self.rooms[ro_uuid].get_equipment() is None:
            self.equipments[eq_uuid].set_room(self.rooms[ro_uuid])
            self.rooms[ro_uuid].set_equipment(self.equipments[eq_uuid])
            self.equipments_rooms[eq_uuid] = ro_uuid
            del self.equipments[eq_uuid]
            return True
        else:
            return False

    def move_equipment_from_room(self, eq_uuid: str):
        ro = self.rooms[self.equipments_rooms[eq_uuid]]
        eq = ro.get_equipment()
        if eq is not None:
            ro.set_equipment(None)
            self.equipments[eq.get_uuid()] = eq
            eq.remove_room()
            del self.equipments_rooms[eq.get_uuid()]
            return True
        else:
            return False

    # купить оборудование
    def buy_service_contract(self, eq_uuid: str):
        if eq_uuid in self.equipments:
            eq = self.equipments[eq_uuid]
        else:
            eq = self.equipments_rooms[eq_uuid]
        if eq is not None:
            if eq.get_service_contract_price() < self.money and eq.can_buy_service_contract():
                self.buy(eq.buy_service_contract())
                return True
            else:
                return False

    def sell_service_contract(self, eq_uuid: str):
        pass

    def buy_lis(self, eq_uuid: str):
        if eq_uuid in self.equipments:
            eq = self.equipments[eq_uuid]
        else:
            eq = self.equipments_rooms[eq_uuid]
        if eq is not None:
            if eq.get_lis_price() < self.money and eq.can_buy_lis():
                self.buy(eq.buy_lis())
                return True
            else:
                return False

    def repair_equipment(self, ro_uuid):
        eq = self.rooms[ro_uuid].get_equipment()
        if eq["state"] == "broken" and self.money >= eq.get_repair_price():
            self.money -= eq.get_repair_price()
            eq.repair_it()
            return True
        return True

    # купить персонал
    def buy_staff(self, ro_uuid: str, staff_type: str):
        ro = self.rooms[ro_uuid]
        staff_info = json.loads(read_file('data/staff.json'))[staff_type]
        if self.money >= staff_info["price"] and \
                ro.get_staff_count()[staff_type] < ro.get_max_staff()[staff_type]:
            self.buy(staff_info["price"])
            ro.add_staff(staff_type)
            return True
        else:
            return False

    #  перемещать персонал
    def move_staff(self, ro_uuid_from: str, ro_uuid_to, staff_type: str):
        ro_from = self.rooms[ro_uuid_from]
        ro_to = self.rooms[ro_uuid_to]
        if ro_from.get_staff_count()[staff_type] > 0 and \
                ro_to.get_staff_count()[staff_type] < ro_to.get_max_staff()[staff_type]:
            ro_from.remove_staff(staff_type)
            ro_to.add_staff(staff_type)
            return True
        else:
            return False

    # купить реагенты

    def buy_reagents(self, eq_uuid: str, amount: int):
        if eq_uuid in self.equipments:
            eq = self.equipments[eq_uuid]
        else:
            eq = self.rooms[self.equipments_rooms[eq_uuid]].get_equipment()

        if eq is not None and self.money >= eq.get_reagent_price() * amount:
            if eq.can_buy_reagents(amount):
                eq.buy_reagents(amount)
                self.buy(eq.get_reagent_price() * amount)
                return True
            return True

    # каждый месяц

    def calc_expenses(self):
        exp = 0
        if self.services["logistic"]:
            exp += 1
        if self.services["training"]:
            exp += 1
        for ro in self.rooms.values():
            exp += ro.get_expenses()
        for eq in self.equipments.values():
            exp += eq.get_expenses()
        return exp

    def calc_power_units(self):
        units: dict = {}
        for ro in self.rooms.values():
            eq = ro.get_equipment()
            if eq is not None:
                un = eq.get_power_units()
                if self.events["power_reduction"]:
                    un.pop()
                units |= un
        return units

    # сделки
    def get_trade_req(self):
        return self.trade_requests

    def add_trade_req(self, trade_request):
        self.trade_requests[trade_request.get_uuid()] = trade_request

    def accept_trade_req(self, trade_uuid):
        self.trade_requests[trade_uuid].accept(self)

    def decline_trade_req(self, trade_uuid):
        self.trade_requests[trade_uuid].decline(self)
