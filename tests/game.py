import unittest
import sys

sys.path.append('../')

from engine.game import Game


class StaticBaseParams(unittest.TestCase):
    game = Game("test")

    def test_rooms_count(self):
        self.assertEqual(60, self.game.rooms)

    def test_staff_count(self):
        self.assertEqual(120, self.game.staff['doctor'])
        self.assertEqual(120, self.game.staff['lab_assistant'])

    def test_equipment_count(self):
        self.assertEqual(12, self.game.equipments['pre_analytic'])
        self.assertEqual(12, self.game.equipments['reporting'])
        self.assertEqual({
            "yellow": 6,
            "red": 6,
            "blue": 6,
            "green": 6,
            "purple": 6,
            "grey": 6
        }, self.game.equipments['hand'])
        self.assertEqual({
            "yellow": 6,
            "red": 6,
            "blue": 6,
            "green": 6,
            "purple": 6,
            "grey": 6
        }, self.game.equipments['semi_manual'])
        self.assertEqual({
            "yellow": 6,
            "red": 6,
            "blue": 6,
            "green": 6,
            "purple": 6,
            "grey": 6
        }, self.game.equipments['auto'])

    def max_pl_count(self):
        self.assertEqual(6, self.game.max_pl_count)
