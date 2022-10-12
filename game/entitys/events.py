import codecs
import copy
import json
import random


class Event:  # Event class
    def generate_dict(self):
        ret = copy.copy(self.__dict__)
        return ret

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def __init__(self, event_data: dict):
        self.name = event_data["name"]
        self.description = event_data["description"]
        self.input = event_data["input"]
        self.code: int = event_data["code"]

    def action(self, obj=None):
        if self.input_type() == "nothing":
            exec("self.action" + str(self.code) + "()")
        exec("self.action" + str(self.code) + "(obj)")

    def input_type(self):
        return self.input

    @staticmethod
    def action0(pl):
        rooms = pl.get_rooms()
        for x in rooms:
            if rooms[x].get_equipment() is not None:
                if rooms[x].get_equipment().get_type() == "reporting":
                    rooms[x].get_equipment().break_it()

    @staticmethod
    def action1(pl):
        pl.events["power_reduction"] = True

    @staticmethod
    def action2(game):
        for x in game.labs:
            lab = game.labs[x]
            for i in lab.orders_correction:
                lab.orders_correction[i] = 1

    @staticmethod
    def action3(pl):
        pass  # TODO: добавить событие

    @staticmethod
    def action4(game):
        for x in game.labs:
            game.labs[x].orders_correction["blue"] = 1

    @staticmethod
    def action5(pl):
        rooms = pl.get_rooms()
        for x in rooms:
            if rooms[x].get_equipment() is not None:
                if rooms[x].get_equipment().get_type() == "pre_analytic":
                    rooms[x].get_equipment().break_it()

    @staticmethod
    def action6(game):
        for x in game.labs:
            game.labs[x].orders_correction["grey"] = 1

    @staticmethod
    def action7(pl):
        rooms = pl.get_rooms().values()
        for x in rooms:
            if x.get_staff()["lab_assistant"] > 0:
                x.staff_count["lab_assistant"] -= 1
                return

    @staticmethod
    def action8(game):
        for x in game.labs:
            game.labs[x].orders_correction["yellow"] = 1

    @staticmethod
    def action9(game):
        for x in game.labs:
            game.labs[x].orders_correction["purple"] = 1

    @staticmethod
    def action10(pl):
        if pl.events["saved_from_negative_analytics"] is False:
            for x in pl.rooms:
                eq = pl.rooms[x].get_equipment()
                if eq is not None:
                    if eq.type == "auto":
                        eq.break_it()
            for x in pl.equipments:
                eq = pl.equipments[x]
                if eq.type == "auto":
                    eq.break_it()

    @staticmethod
    def action11(pl):
        if pl.events["saved_from_negative_analytics"] is False:
            for x in pl.rooms:
                eq = pl.rooms[x].get_equipment()
                if eq is not None:
                    if eq.type == "semi_manual":
                        eq.break_it()
            for x in pl.equipments:
                eq = pl.equipments[x]
                if eq.type == "semi_manual":
                    eq.break_it()

    @staticmethod
    def action12(pl):
        pl.events["need_have_logistic"] = True

    @staticmethod
    def action13(pl):
        if pl.events["saved_from_negative_analytics"] is False:
            for x in pl.rooms:
                eq = pl.rooms[x].get_equipment()
                if eq is not None:
                    if eq.type == "hand":
                        eq.break_it()
            for x in pl.equipments:
                eq = pl.equipments[x]
                if eq.type == "hand":
                    eq.break_it()

    @staticmethod
    def action14():
        pass

    @staticmethod
    def action15(pl):
        pl.events["saved_from_negative_analytics"] = True

    @staticmethod
    def action16(pl):
        if pl.money >= 10:
            pl.money -= 10
        else:
            pl.base_reputation -= 3

    @staticmethod
    def action17(pl):
        rooms = pl.get_rooms().values()
        for x in rooms:
            if x.get_staff()["doctor"] > 0:
                x.staff_count["doctor"] -= 1
                return

    @staticmethod
    def action18(game):
        for x in game.labs:
            lab = game.labs[x]
            for i in lab.orders_correction:
                lab.orders_correction[i] -= 1

    @staticmethod
    def action19(pl):
        pl.base_reputation -= 3

    @staticmethod
    def action20(game):
        for x in game.labs:
            lab = game.labs[x]
            for i in lab.orders_correction:
                lab.orders_correction[i] -= 1

    @staticmethod
    def action21(game):
        for x in game.labs:
            game.labs[x].orders_correction["green"] = 1

    @staticmethod
    def action22(pl):
        pl.events["power_is_calculated"] = True
        pl.events["orders_is_calculated"] = True

    @staticmethod
    def action23(game):
        for x in game.labs:
            game.labs[x].orders_correction["red"] = 1

    @staticmethod
    def action24(pl):
        orders = {
            "blue": 0,
            "grey": 0,
            "yellow": 0,
            "purple": 0,
            "red": 0,
            "green": 0
        }
        for x in pl.rooms:
            eq = pl.rooms[x].get_equipment()
            if eq is not None:
                if eq.type != "reporting" and eq.type != "pre_analytic":
                    orders[eq.get_color()] += eq.get_max_power()

        pl.orders_is_calculated = True
        pl.orders = orders

    @staticmethod
    def action25(pl):
        pl.orders_reputation += 5


def generate_events():
    events = []
    for x in json.loads(codecs.open("data/events.json", encoding='utf-8').read()):
        for i in range(x['amount']):
            events.append(Event(x))
    return events


class Events:


    baseEvents = generate_events()
    events = []

    def __init__(self):
        random.shuffle(self.baseEvents)
        self.events = copy.copy(self.baseEvents)

    def get_event(self):
        if len(self.events) > 0:
            return self.events.pop()
        else:
            random.shuffle(self.baseEvents)
            self.events = copy.copy(self.baseEvents)
            return self.events.pop()
