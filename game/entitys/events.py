import codecs
import copy
import json
import random

from game.entitys.order import Order


class event:  # Event class
    from game.player import Player
    from game.game import Game

    def GetName(self):
        return self.name

    def GetDescription(self):
        return self.description

    def __init__(self, eventData: str):
        self.name = eventData["name"]
        self.description = eventData["description"]
        self.input = eventData["input"]
        self.code: int = eventData["code"]

    def Action(self, obj):
        exec("self.action" + str(self.code) + "(obj)")

    def InputType(self):
        return self.input

    @staticmethod
    def action0(pl: Player):
        rooms = pl.GetRooms()
        for x in rooms:
            if rooms[x].GetEquipment() is not None:
                if rooms[x].GetEquipment().GetType() == "reporting":
                    rooms[x].GetEquipment().Break()

    @staticmethod
    def action1(pl: Player):
        pass

    @staticmethod
    def action2(game: Game):
        for x in game.labs:
            from game.player import Player
            lab: Player = game.labs[x]
            for x in lab.GetOrdersInput():
                if (lab.GetOrdersInput()[x]):
                    order = Order(x, lab.GetUuid())
                    lab.orders[order.GetUuid()] = order

    @staticmethod
    def action3(pl: Player):
        pass

    @staticmethod
    def action4(game: Game):
        for x in game.labs:
            from game.player import Player
            lab: Player = game.labs[x]
            if (lab.GetOrdersInput()["blue"]):
                lab.orders["blue"].append(Order("blue", lab.GetUuid()))

    @staticmethod
    def action5(pl: Player):
        rooms = pl.GetRooms()
        for x in rooms:
            if rooms[x].GetEquipment() is not None:
                if rooms[x].GetEquipment().GetType() is "preanalytic":
                    rooms[x].GetEquipment().Break()

    @staticmethod
    def action6(game: Game):
        for x in game.labs:
            from game.player import Player
            lab: Player = game.labs[x]
            if (lab.GetOrdersInput()["grey"]):
                lab.orders["grey"].append(Order("grey", lab.GetUuid()))

    @staticmethod
    def action7(pl: Player):
        pass

    @staticmethod
    def action8(game: Game):
        for x in game.labs:
            from game.player import Player
            lab: Player = game.labs[x]
            if (lab.GetOrdersInput()["yellow"]):
                lab.orders["yellow"].append(Order("yellow", lab.GetUuid()))

    @staticmethod
    def action9(game: Game):
        for x in game.labs:
            from game.player import Player
            lab: Player = game.labs[x]
            if (lab.GetOrdersInput()["purple"]):
                lab.orders["purple"].append(Order("purple", lab.GetUuid()))


class Events(object):
    baseEvents = [
    ]
    events = []

    def init(self):
        evData = json.loads(codecs.open("data/events.json", encoding='utf-8').read())
        for x in evData:
            for i in range(x['amount']):
                self.baseEvents.append(event(x))
        random.shuffle(self.baseEvents)
        self.events = copy.copy(self.baseEvents)

    def GetEvent(self):
        if len(self.events) > 0:
            return self.events.pop()
        else:
            random.shuffle(self.baseEvents)
            self.events = copy.copy(self.baseEvents)
            return self.events.pop()
