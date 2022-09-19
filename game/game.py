"""Модуль содердит класс @Game"""
import json
from uuid import uuid4

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
        "preanalytic": 12,
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
    def NewLab(self, nickname, password):
        pl = Player(nickname, password)
        self.labs[pl.GetUuid()] = pl
        return pl

    # получение лабораторий
    def GetLab(self, labUuid):
        return self.labs[labUuid]

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
    def BuyRoom(self, labUuid: str):
        if self.rooms > 0 and self.stage == 1 and self.labs[labUuid].CanBuyRoom():
            self.rooms -= 1
            return self.labs[labUuid].BuyRoom()
        else:
            return False

    # купить оборудование
    def BuyEquipment(self, labUuid, roomUuid, equipmentType, equipmentColor, credit: bool):
        lab: Player = self.labs[labUuid]
        equipmentInfo = json.loads(ReadFile('data/equipments.json'))[equipmentType]
        amount: object = self.equipments[equipmentType]
        if equipmentType != "reporting" and equipmentType != "preanalytic":
            amount: int = amount[equipmentColor]

        if amount > 0 and self.stage == 1 and lab.CanBuyEquipment(roomUuid, equipmentInfo):
            if equipmentType != "reporting" and equipmentType != "preanalytic":
                self.equipments[equipmentType][equipmentColor] -= 1
            else:
                self.equipments[equipmentType] -= 1
            lab.Buy(equipmentInfo["price"], credit)

            eq = lab.BuyEquipment(roomUuid, equipmentType, equipmentColor)
            return eq
        else:
            return False

    # купить сервисы

    def BuyLIS(self, labUuid, roomUuid):
        lab = self.labs[labUuid]
        eq = lab.GetRooms()[roomUuid].GetEquipment()
        if eq is not None:
            if lab.GetMoney() >= eq.GetLISPrice() and eq.CanBuyLIS():
                lab.Buy(eq.GetLISPrice())
                eq.BuyLIS()
                return True

    def BuyServiceContract(self, labUuid, roomUuid):
        lab: Player = self.labs[labUuid]
        ro = lab.GetRooms()[roomUuid]
        eq = ro.GetEquipment()
        if (eq is not None):
            if self.services[
                "serviceContract"] > 0 and self.stage == 1 and eq.ServiceContractPrice() < lab.GetMoney() and eq.CanBuyServiceContract():
                self.services["serviceContract"] -= 1
                lab.Buy(eq.BuyServiceContract())
                return
            else:
                return False

    # купить персонал
    def BuyPerson(self, labUuid, roomUuid, personType):
        if self.stage == 1:
            lab = self.labs[labUuid]
            room = lab.GetRooms()[roomUuid]
            personInfo = json.loads(ReadFile('data/persons.json'))[personType]
            if self.persons[personType] > 0 and self.stage == 1 and lab.GetMoney() >= personInfo["price"] and \
                    room.GetPersonsCount()[
                        personType] < room.GetPersonsLimit()[personType]:
                self.persons[personType] -= 1
                lab.Buy(personInfo["price"])
                room.BuyPerson(personType)
            else:
                return False
        else:
            return False

    def SellPerson(self, labUuid, roomUuid, personType):
        if self.stage == 1:
            self.labs[labUuid].GetRooms()[roomUuid].SellPerson(personType)
            self.persons[personType] += 1
            return True
        else:
            return False
    # купить реагент
    def BuyReagents(self, labUuid, roomUuid, amount):
        lab = self.labs[labUuid]
        ro = lab.GetRooms()[roomUuid]
        eq = ro.GetEquipment()
        if eq is not None and self.stage == 1 and lab.GetMoney() >= eq.GetReagentPrice() * amount:
            if eq.CanBuyReagents(amount):
                eq.BuyReagents(amount)
                lab.Buy(eq.GetReagentPrice() * amount)
                return True
            return True

    # powerUnits
    