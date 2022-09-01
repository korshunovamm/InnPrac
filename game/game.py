"""Модуль содердит класс @Game"""
import json

from game.player import Player

gameObject = None


def NewGame():
    """Функция создает новую игру.
    @returntype:Game
    """
    global gameObject
    gameObject = Game()
    return gameObject


def GetGame():
    """Функция возвращает игру.
    @returntype:Game
    """
    return gameObject


def GetLab(labUuid: str) -> dict:
    """Функция возвращает лабораторию по его uuid.
    @param labUuid:str - uuid лабиринта.
    @returntype:dict
    """
    return gameObject.GetLab(labUuid)


def ReadFile(path: str):
    """Функция возвращает содержимое файла.
    @returntype:string
    Функция возвращает содержимое файла распологающегося по относительному пути указанному в path.
    """
    f = open(path, 'r')
    ret = f.read()
    f.close()
    return ret


class Game(object):
    """Класс @Game является коренным классом каждой игры."""
    _day: int = 1
    _stage: int = 1
    _labs = {}
    _events: int = 0
    _rooms: int = 60
    _services = 0
    _equipments: object = {
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
    _persons: object = {
        "doctor": 120,
        "labAssistant": 120
    }

    # конструктор игры
    def __init__(self):
        pass

    # создание новой лаборатории
    def NewLab(self, nickname, password):
        pl = Player(nickname, password)
        self._labs[pl.GetUuid()] = pl
        return pl

    # получение лабораторий
    def GetLab(self, labUuid):
        return self._labs[labUuid]

    # def newStage(self):
    #     sum = 0
    #     for lab in self._labs:
    #         sum += lab.IsReady()
    #     if sum == len(self._labs):
    #         if self._stage == 1:
    #             self._stage = 2
    #             for x in self._labs:
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
    #             self._day += 1
    #             self._stage = 1
    #             for x in self._labs:
    #                 x.NewDay()
    #                 rep = self._labs[x].CalcReputation()
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
    def BuyRoom(self, labUuid):
        if self._rooms > 0 and self._stage == 1 and self._labs[labUuid].CanBuyRoom():
            self._rooms -= 1
            return self._labs[labUuid].BuyRoom()
        else:
            return False

    # купить оборудование
    def BuyEquipment(self, labUuid, roomUuid, equipmentType, equipmentColor):
        lab: Player = self._labs[labUuid]
        equipmentInfo = json.loads(ReadFile('data/equipments.json'))[equipmentType]
        amount = self._equipments[equipmentType]
        if equipmentType != "reporting" and equipmentType != "pre_analytic":
            amount = amount[equipmentColor]

        if amount > 0 and self._stage == 1 and lab.CanBuyEquipment(roomUuid, equipmentInfo):
            if equipmentType != "reporting" and equipmentType != "pre_analytic":
                self._equipments[equipmentType][equipmentColor] -= 1
            else:
                self._equipments[equipmentType] -= 1
            lab.Buy(equipmentInfo["price"])

            eq = lab.BuyEquipment(roomUuid, equipmentType, equipmentColor)
            return eq
        else:
            return False

    # купить персонал
    def BuyPerson(self, labUuid, roomUuid, personType):
        lab = self._labs[labUuid]
        room = lab.GetRooms()[roomUuid]
        personInfo = json.loads(ReadFile('data/persons.json'))[personType]
        if self._persons[personType] > 0 and self._stage == 1 and lab.GetMoney() >= personInfo["price"] and \
                room.GetPersonCount()[
                    personType] < room.GetPersonsLimit()[personType]:
            room.BuyPerson(personType)
        else:
            return False
