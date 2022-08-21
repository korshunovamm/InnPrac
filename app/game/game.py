import json


class Game:
    _labs = []
    _events = 0
    _rooms = 10
    _services = 0
    _equipments = 0
    _persons = 0
    def __init__(self):
        f = open('data/events.json', 'r')
        self._events = json.loads(f.read())
        f.close()
        f = open('data/services.json', 'r')
        self._service = json.loads(f.read())
        f.close()
        f = open('data/equipments.json', 'r')
        self._service = json.loads(f.read())
        f.close()
