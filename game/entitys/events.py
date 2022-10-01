import codecs
import copy
import json
import random

from game.entitys.order import Order


class Event:  # Event class
    from game.player import Player
    from game.game import Game

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def __init__(self, event_data: dict):
        self.name = event_data["name"]
        self.description = event_data["description"]
        self.input = event_data["input"]
        self.code: int = event_data["code"]

    def action(self, obj):
        exec("self.action" + str(self.code) + "(obj)")

    def input_type(self):
        return self.input

    @staticmethod
    def action0(pl: Player):
        rooms = pl.get_rooms()
        for x in rooms:
            if rooms[x].get_equipment() is not None:
                if rooms[x].get_equipment().get_type() == "reporting":
                    rooms[x].get_equipment().break_it()

    @staticmethod
    def action1(pl: Player):
        pass

    @staticmethod
    def action2(game: Game):
        for x in game.labs:
            from game.player import Player
            lab: Player = game.labs[x]
            for i in lab.get_orders_input():
                if lab.get_orders_input()[i]:
                    order = Order(i, lab.get_uuid())
                    lab.orders[order.get_uuid()] = order

    @staticmethod
    def action3(pl: Player):
        pass

    @staticmethod
    def action4(game: Game):
        for x in game.labs:
            from game.player import Player
            lab: Player = game.labs[x]
            if lab.get_orders_input()["blue"]:
                lab.orders["blue"].append(Order("blue", lab.get_uuid()))

    @staticmethod
    def action5(pl: Player):
        rooms = pl.get_rooms()
        for x in rooms:
            if rooms[x].get_equipment() is not None:
                if rooms[x].get_equipment().get_type() is "pre_analytic":
                    rooms[x].get_equipment().break_it()

    @staticmethod
    def action6(game: Game):
        for x in game.labs:
            from game.player import Player
            lab: Player = game.labs[x]
            if lab.get_orders_input()["grey"]:
                lab.orders["grey"].append(Order("grey", lab.get_uuid()))

    @staticmethod
    def action7(pl: Player):
        pass

    @staticmethod
    def action8(game: Game):
        for x in game.labs:
            from game.player import Player
            lab: Player = game.labs[x]
            if lab.get_orders_input()["yellow"]:
                lab.orders["yellow"].append(Order("yellow", lab.get_uuid()))

    @staticmethod
    def action9(game: Game):
        for x in game.labs:
            from game.player import Player
            lab: Player = game.labs[x]
            if lab.get_orders_input()["purple"]:
                lab.orders["purple"].append(Order("purple", lab.get_uuid()))


class Events(object):
    baseEvents = [
    ]
    events = []

    def __init__(self):
        for x in json.loads(codecs.open("data/events.json", encoding='utf-8').read()):
            for i in range(x['amount']):
                self.baseEvents.append(Event(x))
        random.shuffle(self.baseEvents)
        self.events = copy.copy(self.baseEvents)

    def get_event(self):
        if len(self.events) > 0:
            return self.events.pop()
        else:
            random.shuffle(self.baseEvents)
            self.events = copy.copy(self.baseEvents)
            return self.events.pop()
