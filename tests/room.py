import random
import unittest
from math import inf
import sys

sys.path.append('../')

from engine.entitys.room import Room
from engine.game import Game


class Buy(unittest.TestCase):

    def test_rooms_count_ok(self):  # купить до 10 помещений
        game = Game("test")
        pl = game.new_lab("test")
        ro_count = random.randint(1, 10)
        for i in range(ro_count):
            game.buy_room(pl.get_uuid())
        self.assertEqual(ro_count, len(pl.get_rooms()))
        self.assertEqual(60 - ro_count, game.rooms)
        self.assertEqual(120 - ro_count * 10, pl.get_money())

    def test_room_buy(self):  # купить слишком много помещений
        game = Game("test")
        pl = game.new_lab("test")
        pl.money = 1000
        ro_count = random.randint(1, 10) + 60
        for i in range(ro_count):
            game.buy_room(pl.get_uuid())
        self.assertEqual(60, len(pl.get_rooms()))
        self.assertEqual(0, game.rooms)
        self.assertEqual(400, pl.get_money())

    def test_room_buy_2pl(self):
        game = Game("test")
        pl = game.new_lab("test")
        pl.money = inf
        pl2 = game.new_lab("test")
        pl2.money = inf
        ro_count1 = random.randint(1, 10)
        for i in range(ro_count1):
            game.buy_room(pl.get_uuid())
        ro_count2 = random.randint(1, 10)
        for i in range(ro_count2):
            game.buy_room(pl2.get_uuid())
        self.assertEqual(ro_count1, len(pl.get_rooms()))
        self.assertEqual(ro_count2, len(pl2.get_rooms()))
        self.assertEqual(60 - ro_count1 - ro_count2, game.rooms)


class Sell(unittest.TestCase):
    def test_sell_room(self):
        game = Game("test")
        pl = game.new_lab("test")
        ro_count = random.randint(1, 10)
        res = True
        for x in range(ro_count):
            ro = game.buy_room(pl.get_uuid())[1]
            r = game.sell_room(pl.get_uuid(), ro.get_uuid())
            if r is False:
                res = False
        self.assertEqual(0, len(pl.get_rooms()))
        self.assertEqual(60, game.rooms)
        self.assertEqual(120 - ro_count * 5, pl.get_money())
        self.assertTrue(res)


class StaticBaseParams(unittest.TestCase):

    ro = Room()

    def test_price(self):
        self.assertEqual(10, self.ro.get_price())

    def test_reputation(self):
        self.assertEqual(1, self.ro.get_base_reputation())

    def test_expenses(self):
        self.assertEqual(3, self.ro.get_base_expenses())


# class Staff(unittest.TestCase):
#     def test_buy_staff(self):
#         manage_game = Game("test")
#         pl = manage_game.new_lab("test")
#         ro = manage_game.buy_room(pl.get_uuid())
#         print(pl.money)
#         for x in range(10):
#             manage_game.buy_staff(4, ro.get_staff_count()["lab_assistant"])
#         self.assertEqual(106, pl.get_money())
