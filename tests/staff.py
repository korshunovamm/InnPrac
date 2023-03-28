import unittest
import sys

sys.path.append('../')

from engine.game import Game


class Buy(unittest.TestCase):
    def test_buy_staff(self):
        game = Game("test")
        pl = game.new_lab("test")
        ro = game.buy_room(pl.get_uuid())[1]
        eq = game.buy_equipment(pl.get_uuid(), "auto", "blue", False)[1]
        game.move_equipment_to_room(pl.get_uuid(), ro.get_uuid(), eq.get_uuid())
        for x in range(4):
            game.buy_staff(pl.get_uuid(), ro.get_uuid(), "doctor")
            game.buy_staff(pl.get_uuid(), ro.get_uuid(), "lab_assistant")
        self.assertEqual(4, ro.staff_count["doctor"])
        self.assertEqual(4, ro.staff_count["lab_assistant"])
        self.assertEqual(116, game.staff["doctor"])
        self.assertEqual(116, game.staff["lab_assistant"])

    def test_buy_staff_all(self):
        game = Game("test")
        pl = game.new_lab("test")
        ro = game.buy_room(pl.get_uuid())[1]
        game.staff["doctor"] = 4
        game.staff["lab_assistant"] = 4
        eq = game.buy_equipment(pl.get_uuid(), "auto", "blue", False)[1]
        game.move_equipment_to_room(pl.get_uuid(), ro.get_uuid(), eq.get_uuid())
        for x in range(4):
            game.buy_staff(pl.get_uuid(), ro.get_uuid(), "doctor")
            game.buy_staff(pl.get_uuid(), ro.get_uuid(), "lab_assistant")
        self.assertEqual(4, ro.staff_count["doctor"])
        self.assertEqual(4, ro.staff_count["lab_assistant"])
        self.assertEqual(0, game.staff["doctor"])
        self.assertEqual(0, game.staff["lab_assistant"])

    def test_buy_staff_not_enough(self):  # не хватает людей
        game = Game("test")
        pl = game.new_lab("test")
        ro = game.buy_room(pl.get_uuid())[1]
        game.staff["doctor"] = 0
        game.staff["lab_assistant"] = 0
        eq = game.buy_equipment(pl.get_uuid(), "auto", "blue", False)[1]
        game.move_equipment_to_room(pl.get_uuid(), ro.get_uuid(), eq.get_uuid())
        for x in range(4):
            game.buy_staff(pl.get_uuid(), ro.get_uuid(), "doctor")
            game.buy_staff(pl.get_uuid(), ro.get_uuid(), "lab_assistant")
        self.assertEqual(0, ro.staff_count["doctor"])
        self.assertEqual(0, ro.staff_count["lab_assistant"])
        self.assertEqual(0, game.staff["doctor"])
        self.assertEqual(0, game.staff["lab_assistant"])
        self.assertEqual(120 - 10 - 60, pl.get_money())

    def test_buy_staff_to_much(self):  # слишком много людей
        game = Game("test")
        pl = game.new_lab("test")
        ro = game.buy_room(pl.get_uuid())[1]
        for x in range(4):
            game.buy_staff(pl.get_uuid(), ro.get_uuid(), "doctor")
            game.buy_staff(pl.get_uuid(), ro.get_uuid(), "lab_assistant")
        res = game.buy_staff(pl.get_uuid(), ro.get_uuid(), "doctor")[0]
        res2 = game.buy_staff(pl.get_uuid(), ro.get_uuid(), "lab_assistant")[0]
        res = res == res2 and res is False
        self.assertEqual({
            "doctor": 4,
            "lab_assistant": 4
        }, ro.staff_count)
        self.assertEqual(True, res)