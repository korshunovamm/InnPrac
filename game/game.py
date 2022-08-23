"""Модуль содердит класс @Game"""
from game.player import Player


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
    _day = 1
    _stage = 1
    _labs = []
    _events = 0
    _rooms = 10
    _services = 0
    _equipments = 0
    _persons = 0

    def __init__(self):
        print(str(object))
        self._events = ReadFile('data/events.json')
        self._services = ReadFile('data/services.json')
        self._equipments = ReadFile('data/equipments.json')

    def NewLab(self, nickname, password):
        pl = Player(nickname, password)
        self._labs.append(pl)
        return pl.GetUuid()

    def newStage(self):
        if self._stage == 1:
            self._stage = 2
            for x in self._labs:
                OrderLevel = None
                rep = x.FirstStep(self._events)["Reputation"]
                if rep < 10:
                    OrderLevel = 0
                elif rep < 20:
                    OrderLevel = 1
                elif rep < 30:
                    OrderLevel = 2
                elif rep < 40:
                    OrderLevel = 3
                else:
                    OrderLevel = 4
                x.CalcOrdersCount(OrderLevel)
        else:
            self._day += 1
            self._stage = 1
