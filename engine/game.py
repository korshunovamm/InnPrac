import copy
import json
from uuid import uuid4

from engine.entitys.events import Events
from engine.player import Player
from engine.deal import TradeReq, PledgeReq


def read_file(path: str):
    f = open(path, 'r')
    ret = f.read()
    f.close()
    return ret


class Game(object):
    def get_uuid(self):
        return self.uuid

    def get_name(self):
        return self.name

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    max_pl_count: int = 6

    def generate_dict(self):
        ret = copy.copy(self.__dict__)
        ret['labs'] = {}
        for x in self.labs:
            ret['labs'][x] = self.labs[x].generate_dict()
        del ret['pledges']
        del ret['bank_pledges']
        del ret['events_deck']
        return ret

    # конструктор игры
    def __init__(self, name: str):
        self.pledges = {}  # залоги игроков, при переходе с 2 на 1 стадию, проверяем что они не просрочены и не отменены
        self.bank_pledges = {}  # залоги в банке
        self.credits = 12
        self.month: int = 1
        self.stage: int = 1
        self.uuid: str = uuid4().hex
        self.labs: dict[str, Player] = {}
        self.events_deck: Events = Events()
        self.rooms: int = 60
        self.equipments: dict[str, int or dict[str, int]] = {
            'hand': {
                'yellow': 6,
                'red': 6,
                'blue': 6,
                'green': 6,
                'purple': 6,
                'grey': 6
            },
            'semi_manual': {
                'yellow': 6,
                'red': 6,
                'blue': 6,
                'green': 6,
                'purple': 6,
                'grey': 6
            },
            'auto': {
                'yellow': 6,
                'red': 6,
                'blue': 6,
                'green': 6,
                'purple': 6,
                'grey': 6
            },
            'pre_analytic': 12,
            'reporting': 12
        }
        self.staff: dict[str, int] = {
            'doctor': 120,
            'lab_assistant': 120
        }
        self.name: str = name
        self.status = 'waiting'

    # кол-во людей в игре
    def get_max_players(self):
        return self.max_pl_count

    def get_players_count(self):
        return len(self.labs)

    # создание новой лаборатории
    def new_lab(self, pl_name):
        if len(self.labs) < self.max_pl_count:
            pl = Player(pl_name)
            self.labs[pl.get_uuid()] = pl
            if len(self.labs) == self.max_pl_count:
                self.status = 'full'
            return pl
        else:
            return False

    def remove_lab(self, lab_uuid):
        if lab_uuid in self.labs:
            del self.labs[lab_uuid]
            return True
        else:
            return False

    def transition_to_stage_2(self):
        if self.stage == 1:
            self.stage = 2
            for lab in self.labs:
                ev = self.events_deck.get_event()
                self.labs[lab].last_event = ev
                if ev.get_input_type() == 'nothing':
                    ev.action()
                elif ev.get_input_type() == 'ga':
                    ev.action(self)
                elif ev.get_input_type() == 'pl':
                    ev.action(self.labs[lab])
                else:
                    ev.action(self, self.labs[lab])
            for x in self.labs:
                lab = self.labs[x]
                rep = lab.calc_reputation()
                if rep < 10:
                    order_level = 0
                elif rep < 20:
                    order_level = 1
                elif rep < 30:
                    order_level = 2
                elif rep < 40:
                    order_level = 3
                else:
                    order_level = 4
                lab.calc_orders_count(order_level)
                lab.calc_power()
                if lab.pay_type == 'pre_pay':
                    lab.sell(len(lab.orders) * 20)
                return True
        else:
            return False

    def transition_to_stage_1(self):
        if self.stage == 2:
            self.stage = 1
            self.month += 1
            for lab in self.labs:
                self.labs[lab].calc_orders_reputation()
                self.labs[lab].orders_refund()
                self.labs[lab].dump_params()
                self.labs[lab].buy(self.labs[lab].calc_expenses())
                for x in self.labs[lab].rooms:
                    eq = self.labs[lab].rooms[x].get_equipment()
                    if eq is not None:
                        eq.reset_selled_power()
            pledges = copy.copy(self.pledges)
            for x in pledges:
                if self.pledges[x].end_month < self.month:
                    self.pledges[x].execute_give_bail()
                    del self.pledges[x]
                elif self.pledges[x].get_status() == 'canceled':
                    del self.pledges[x]
            for x in self.bank_pledges:
                if self.pledges[x].get_status() == 'canceled':
                    del self.pledges[x]
        else:
            return False

    # купить комнату
    def buy_room(self, lab_uuid: str):
        if self.rooms > 0 and self.stage == 1 and self.labs[lab_uuid].can_buy_room():
            self.rooms -= 1
            return True, self.labs[lab_uuid].buy_room()
        else:
            return False, None

    # продать комнату

    def sell_room(self, lab_uuid, room_uuid):
        res = self.labs[lab_uuid].sell_room(room_uuid)
        if res is not False:
            self.rooms += 1
        return res

    def buy_equipment(self, lab_uuid, eq_type, eq_color, credit: bool):
        lab: Player = self.labs[lab_uuid]
        equipment_info = json.loads(read_file('data/equipments.json'))[eq_type]
        amount: int = self.equipments[eq_type]
        if eq_type not in ['reporting', 'pre_analytic']:
            amount: int = amount[eq_color]
        if amount > 0 and self.stage == 1 and lab.can_buy_equipment(equipment_info):
            if eq_type not in ['reporting', 'pre_analytic']:
                self.equipments[eq_type][eq_color] -= 1
            else:
                self.equipments[eq_type] -= 1
            if credit and self.credits > 0 or not credit:
                if credit:
                    self.credits -= 1
                eq = lab.buy_equipment(eq_type, eq_color)
                lab.buy(equipment_info['price'], credit)
                return True, eq
            else:
                return False, None
        else:
            return False, None

    # продать оборудование
    def sell_equipment(self, lab_uuid, eq_uuid):
        if self.stage == 1:
            res = self.labs[lab_uuid].sell_equipment(eq_uuid)
            if res is not False:
                if res[1] not in ['reporting', 'pre_analytic']:
                    self.equipments[res[1]][res[2]] += 1
                else:
                    self.equipments[res[1]] += 1
                return True
            return False
        else:
            return False

    # переместить оборудование
    def move_equipment_to_room(self, lab_uuid, room_uuid, eq_uuid):
        return self.labs[lab_uuid].move_equipment_to_room(eq_uuid, room_uuid)

    def move_equipment_from_room(self, lab_uuid, room_uuid):
        return self.labs[lab_uuid].move_equipment_from_room(room_uuid)

    # купить сервисы

    def buy_lis(self, lab_uuid, eq_uuid):
        lab = self.labs[lab_uuid]
        if self.stage == 1 and lab.can_buy_lis(eq_uuid):
            eq = lab.get_equipment(eq_uuid)
            eq.buy_lis()
            return True, eq
        else:
            return False, None

    def buy_service_contract(self, pl_uuid, eq_uuid):
        if self.stage == 1:
            return self.labs[pl_uuid].buy_service_contract(eq_uuid)

    def buy_service_maintenance(self, pl_uuid, eq_uuid):
        if self.stage == 1:
            return self.labs[pl_uuid].buy_service_maintenance(eq_uuid)

    # купить персонал

    def buy_staff(self, pl_uuid, ro_uuid, staff_type, amount):
        if self.stage == 1 and self.staff[staff_type] > 0:
            pl = self.labs[pl_uuid]
            if pl.buy_staff(ro_uuid, staff_type, amount):
                self.staff[staff_type] -= 1
                return True, pl.get_room(ro_uuid)
            else:
                return False, None
        else:
            return False, None

    # продать персонал
    def sell_staff(self, lab_uuid, ro_uuid, staff_type):
        ro = self.labs[lab_uuid].get_room(ro_uuid)
        if self.stage == 1 and ro is not None and ro.get_staff()[staff_type] > 0:
            self.labs[lab_uuid].get_room(ro_uuid).remove_staff(staff_type)
            self.staff[staff_type] += 1
            return True, ro
        else:
            return False, None

    # взаимодействие игроков
    # новая сделка
    def new_trade_req(self, pl_0_uuid, pl_1_uuid, pl_0_items, pl_1_items):
        if self.stage == 1:
            trade = TradeReq(self.labs[pl_0_uuid], self.labs[pl_1_uuid], pl_0_items, pl_1_items)
            self.labs[pl_0_uuid].add_trade_req(trade)
            self.labs[pl_1_uuid].add_trade_req(trade)
            return True, trade
        else:
            return False, None

    # принять сделку
    def accept_trade_req(self, pl_uuid, trade_uuid):
        if self.stage == 1:
            self.labs[pl_uuid].accept_trade_req(trade_uuid)
            return True
        else:
            return False

    # отклонить сделку
    def decline_trade_req(self, pl_uuid, trade_uuid):
        if self.stage == 1:
            self.labs[pl_uuid].decline_trade_req(trade_uuid)
            return True
        else:
            return False

    # новый залог
    def new_pledge_req(self, pl_0_uuid, pl_1_uuid, purchase_price, redemption_price, items, duration):
        if self.stage == 1:
            pledge = PledgeReq(self.labs[pl_0_uuid], self.labs[pl_1_uuid], purchase_price, redemption_price, items,
                               self.month + duration)
            self.pledges[pledge.get_uuid()] = pledge
            return True, pledge
        else:
            return False, None

    # купить реагент
    def buy_reagents(self, lab_uuid, eq_uuid, amount):
        if self.stage == 1:
            return self.labs[lab_uuid].buy_reagents(eq_uuid, amount), self.labs[lab_uuid].get_equipment(eq_uuid)
        else:
            return False, None
