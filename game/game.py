import json
from uuid import uuid4

from game.player import Player


def read_file(path: str):
    f = open(path, 'r')
    ret = f.read()
    f.close()
    return ret


class Game(object):
    """Класс @Game является коренным классом каждой игры."""
    day: int = 1
    stage: int = 1
    uuid: str = uuid4().hex
    labs = {}
    events: int = 0
    rooms: int = 60
    equipments: object = {
        "hand": {
            "yellow": 6,
            "red": 6,
            "blue": 6,
            "green": 6,
            "purple": 6,
            "grey": 6
        },
        "semi-manual": {
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
    persons: object = {
        "doctor": 120,
        "labAssistant": 120
    }
    services = {
        "serviceContract": 12  # TODO: заменить на значение которое папа пришлет
    }

    # конструктор игры
    def __init__(self):
        pass

    # создание новой лаборатории
    def new_lab(self, nickname, password):
        pl = Player(nickname, password)
        self.labs[pl.get_uuid()] = pl
        return pl

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
    pass

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
                lab.buy(equipment_info["price"], credit)
            return eq
        else:
            return False

    # продать оборудование
    def sell_equipment(self, lab_uuid, eq_uuid):
        lab: Player = self.labs[lab_uuid]
        lab.sell_equipment(eq_uuid)
        return self.labs[lab_uuid].sell(eq_uuid)

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
        if self.services["serviceContract"] > 0 and self.stage == 1:
            if self.labs[pl_uuid].buy_service_contract(eq_uuid):
                self.services["serviceContract"] -= 1
                return True
            else:
                return False

    # купить персонал
    def buy_person(self, pl_uuid, ro_uuid, person_type):
        if self.stage == 1:
            if self.labs[pl_uuid].buy_person(ro_uuid, person_type):
                self.persons[person_type] -= 1
                return True
            else:
                return False
        else:
            return False

    def sell_person(self, lab_uuid, ro_uuid, person_type):
        if self.stage == 1:
            self.labs[lab_uuid].get_rooms()[ro_uuid].sell_person(person_type)
            self.persons[person_type] += 1
            return True
        else:
            return False

    # купить реагент
    def buy_reagents(self, lab_uuid, ro_uuid, amount):
        lab = self.labs[lab_uuid]
        ro = lab.get_rooms()[ro_uuid]
        eq = ro.get_equipment()
        if eq is not None and self.stage == 1 and lab.get_money() >= eq.get_reagent_price() * amount:
            if eq.can_buy_reagents(amount):
                eq.buy_reagents(amount)
                lab.buy(eq.get_reagent_price() * amount)
                return True
            return True

    # powerUnits
