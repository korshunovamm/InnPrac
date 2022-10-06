import json
from uuid import uuid4

from game.entitys.events import Events
from game.player import Player
from game.deal import TradeReq


def read_file(path: str):
    f = open(path, 'r')
    ret = f.read()
    f.close()
    return ret


class Game(object):
    max_pl_count: int = 6

    # конструктор игры
    def __init__(self):
        self.credits = 12
        self.day: int = 1
        self.stage: int = 1
        self.uuid: str = uuid4().hex
        self.labs = {}
        self.events = Events()
        self.rooms: int = 60
        self.equipments: object = {
            "hand": {
                "yellow": 6,
                "red": 6,
                "blue": 6,
                "green": 6,
                "purple": 6,
                "grey": 6
            },
            "semi_manual": {
                "yellow": 6,
                "red": 6,
                "blue": 6,
                "green": 6,
                "purple": 6,
                "grey": 6
            },
            "auto": {
                "yellow": 6,
                "red": 6,
                "blue": 6,
                "green": 6,
                "purple": 6,
                "grey": 6
            },
            "pre_analytic": 12,
            "reporting": 12
        }
        self.staff: object = {
            "doctor": 120,
            "lab_assistant": 120
        }

    # создание новой лаборатории
    def new_lab(self, nickname, password):
        if len(self.labs) < self.max_pl_count:
            pl = Player(nickname, password)
            self.labs[pl.get_uuid()] = pl
            return pl
        else:
            return False

    # получение лабораторий

    # def newStage(self):
    #     sum = 0
    #     for lab in self.labs:
    #         sum += lab.IsReady()
    #     if sum == len(self.labs):
    #         if self.stage == 1:
    #             self.stage = 2
    #             for x in self.labs:
    #                 rep = x.CalcReputation()
    #                 if rep < 10:
    #                     orderLevel = 0
    #                 elif rep < 20:
    #                     orderLevel = 1
    #                 elif rep < 30:
    #                     orderLevel = 2
    #                 elif rep < 40:
    #                     orderLevel = 3
    #                 else:
    #                     orderLevel = 4
    #                 x.CalcOrdersCount(orderLevel)
    #         else:
    #             self.day += 1
    #             self.stage = 1
    #             for x in self.labs:
    #                 x.NewDay()
    #                 rep = self.labs[x].CalcReputation()
    #                 if rep < 10:
    #                     orderLevel = 0
    #                 elif rep < 20:
    #                     orderLevel = 1
    #                 elif rep < 30:
    #                     orderLevel = 2
    #                 elif rep < 40:
    #                     orderLevel = 3
    #                 else:
    #                     orderLevel = 4
    #                 x.CalcOrdersCount(orderLevel)

    # купить комнату
    def buy_room(self, lab_uuid: str):
        if self.rooms > 0 and self.stage == 1 and self.labs[lab_uuid].can_buy_room():
            self.rooms -= 1
            return self.labs[lab_uuid].buy_room()
        else:
            return False

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
        if eq_type != "reporting" and eq_type != "pre_analytic":
            amount: int = amount[eq_color]

        if amount > 0 and self.stage == 1 and lab.can_buy_equipment(equipment_info):
            if eq_type != "reporting" and eq_type != "pre_analytic":
                self.equipments[eq_type][eq_color] -= 1
            else:
                self.equipments[eq_type] -= 1
            eq = lab.buy_equipment(eq_type, eq_color)
            if eq is not False:
                if credit and self.credits > 0:
                    self.credits -= 1
                    lab.buy(equipment_info["price"], credit)
                    return eq, True
                else:
                    lab.buy(equipment_info["price"])
                    return eq, False
        else:
            return False

    # продать оборудование
    def sell_equipment(self, lab_uuid, eq_uuid):
        if self.stage == 1:
            res = self.labs[lab_uuid].sell_equipment(eq_uuid)
            if res[0] != "reporting" and res[0] != "pre_analytic":
                self.equipments[res[0]][res[1]] += 1
            else:
                self.equipments[res[0]] += 1
            return res

    # переместить оборудование
    def move_equipment_to_room(self, lab_uuid, room_uuid, eq_uuid):
        return self.labs[lab_uuid].move_equipment_to_room(eq_uuid, room_uuid)

    def move_equipment_from_room(self, lab_uuid, room_uuid):
        return self.labs[lab_uuid].move_equipment_from_room(room_uuid)
    # купить сервисы

    def buy_lis(self, lab_uuid, ro_uuid):
        lab = self.labs[lab_uuid]
        eq = lab.get_rooms()[ro_uuid].get_equipment()
        if eq is not None:
            if lab.get_money() >= eq.get_lis_price() and eq.can_buy_lis():
                lab.buy(eq.get_lis_price())
                eq.buy_lis()
                return True

    def buy_service_contract(self, pl_uuid, eq_uuid):
        if self.stage == 1:
            return self.labs[pl_uuid].buy_service_contract(eq_uuid)

    # купить персонал
    def buy_staff(self, pl_uuid, ro_uuid, staff_type):
        if self.stage == 1 and self.staff[staff_type] > 0:
            if self.labs[pl_uuid].buy_staff(ro_uuid, staff_type):
                self.staff[staff_type] -= 1
                return True
            else:
                return False
        else:
            return False

    # продать персонал
    def sell_staff(self, lab_uuid, ro_uuid, staff_type):
        if self.stage == 1:
            self.labs[lab_uuid].get_rooms()[ro_uuid].sell_staff(staff_type)
            self.staff[staff_type] += 1
            return True
        else:
            return False

    # взаимодействие игроков
    # новая сделка
    def new_trade_req(self, pl_0_uuid, pl_1_uuid, pl_0_items, pl_1_items):
        if self.stage == 1:
            trade = TradeReq(self.labs[pl_0_uuid], pl_0_items, pl_1_items)
            self.labs[pl_0_uuid].add_trade_req(trade)
            self.labs[pl_1_uuid].add_trade_req(trade)
            return True
        else:
            return False

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
    # купить реагент
    def buy_reagents(self, lab_uuid, eq_uuid, amount):
        if self.stage == 1:
            return self.labs[lab_uuid].buy_reagents(eq_uuid, amount)
        else:
            return False
    # powerUnits
