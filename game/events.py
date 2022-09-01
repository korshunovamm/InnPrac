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
                    print(rooms[x].GetEquipment().GetBreaked())

    @staticmethod
    def action1(pl: Player):
        pass

    @staticmethod
    def action2(pl: Player):
        pass

    @staticmethod
    def action3(pl: Player):
        pass

    @staticmethod
    def action4(game: Game):
        pass

    @staticmethod
    def action5(pl: Player):
        pass

    @staticmethod
    def action6(game: Game):
        pass

    @staticmethod
    def action7(pl: Player):
        pass

    @staticmethod
    def action8(game: Game):
        pass

    @staticmethod
    def action9(game: Game):
        for x in game._labs:
            from game.player import Player
            lab: Player = game._labs[x]
            if (lab.GetOrdersInput()["purple"]):
                lab._ordorders["purple"].append(Order("purple", lab.GetUuid()))


class events(object):
    _baseEvents = [
    ]
    _events = []

    def __init__(self):
        evData = json.loads(codecs.open("data/events.json", encoding='utf-8').read())
        for x in evData:
            for i in range(x['amount']):
                self._baseEvents.append(event(x))
        random.shuffle(self._baseEvents)
        self._events = copy.copy(self._baseEvents)

    def GetEvent(self):
        if len(self._events) > 0:
            return self._events.pop()
        else:
            random.shuffle(self._baseEvents)
            self._events = copy.copy(self._baseEvents)
            return self._events.pop()
