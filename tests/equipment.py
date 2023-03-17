import unittest

from engine.game import Game


class Buy(unittest.TestCase):
    def test_buy(self):
        game = Game("test")
        pl = game.new_lab("test")
        eq = game.buy_equipment(pl.get_uuid(), "auto", "blue", False)[1]
        self.assertEqual(eq.get_type(), "auto")
        self.assertEqual(eq.get_color(), "blue")
        self.assertIn(eq.get_uuid(), pl.equipments)

    def test_buy_to_much(self):
        game = Game("test")
        pl = game.new_lab("test")
        pl.money = 10000
        for x in range(10):
            game.buy_equipment(pl.get_uuid(), "auto", "blue", False)
            game.buy_equipment(pl.get_uuid(), "auto", "red", False)
        self.assertEqual(len(pl.equipments), 12)
        self.assertEqual(game.equipments['auto']['blue'], 0)
        self.assertEqual(game.equipments['auto']['red'], 0)
        self.assertEqual(game.equipments['auto']['grey'], 6)
        self.assertEqual(pl.money, 10000 - 12 * 60)

    def test_buy_credit(self):
        game = Game("test")
        pl = game.new_lab("test")
        pl.money = 10000
        eq = game.buy_equipment(pl.get_uuid(), "auto", "blue", True)[1]
        self.assertEqual("auto", eq.get_type())
        self.assertEqual("blue", eq.get_color())
        self.assertIn(eq.get_uuid(), pl.equipments)
        self.assertEqual(10000, pl.money)
        self.assertEqual(11, game.credits)

    def test_buy_to_much_credit(self):
        game = Game("test")
        pl = game.new_lab("test")
        pl.money = 10000
        for x in range(10):
            game.buy_equipment(pl.get_uuid(), "pre_analytic", None, True)
            game.buy_equipment(pl.get_uuid(), "reporting", None, True)
        self.assertEqual(len(pl.equipments), 12)
        self.assertEqual(10000, pl.money)
        self.assertEqual(0, game.credits)


class Sell(unittest.TestCase):
    def test_sell(self):
        game = Game("test")
        pl = game.new_lab("test")
        eq = game.buy_equipment(pl.get_uuid(), "auto", "blue", False)[1]
        game.sell_equipment(pl.get_uuid(), eq.get_uuid())
        self.assertEqual(len(pl.equipments), 0)
        self.assertEqual(game.equipments['auto']['blue'], 6)
        self.assertEqual(90, pl.money)


class Move(unittest.TestCase):

    def test_move_to_room(self):
        game = Game("test")
        pl = game.new_lab("test")
        ro = game.buy_room(pl.get_uuid())[1]
        eq = game.buy_equipment(pl.get_uuid(), "pre_analytic", None, False)[1]
        game.move_equipment_to_room(pl.get_uuid(), ro.get_uuid(), eq.get_uuid())
        self.assertIsNotNone(ro.get_equipment())
        self.assertEqual(ro.get_equipment(), eq)
        self.assertEqual(ro.get_uuid(), pl.equipments_rooms[eq.get_uuid()])

    def test_move_from_room(self):
        game = Game("test")
        pl = game.new_lab("test")
        ro = game.buy_room(pl.get_uuid())[1]
        eq = game.buy_equipment(pl.get_uuid(), "pre_analytic", None, False)[1]
        game.move_equipment_to_room(pl.get_uuid(), ro.get_uuid(), eq.get_uuid())
        game.move_equipment_from_room(pl.get_uuid(), eq.get_uuid())
        self.assertEqual(11, game.equipments["pre_analytic"])
        self.assertIsNone(ro.get_equipment())
        self.assertEqual(pl.equipments[eq.get_uuid()], eq)


class BuyReagents(unittest.TestCase):

    def test_buy_reagents(self):
        game = Game("test")
        pl_uuid = game.new_lab("test").get_uuid()
        ro_uuid = game.buy_room(pl_uuid)[1].get_uuid()
        eq_uuid = game.buy_equipment(pl_uuid, "auto", "blue", False)[1].get_uuid()
        for x in range(4):
            game.buy_staff(pl_uuid, ro_uuid, "doctor")
            game.buy_staff(pl_uuid, ro_uuid, "lab_assistant")
        game.move_equipment_to_room(pl_uuid, ro_uuid, eq_uuid)
        game.buy_reagents(pl_uuid, eq_uuid, 3)
        pass
        self.assertEqual(3, game.labs[pl_uuid].rooms[ro_uuid].get_equipment().get_reagents())
        self.assertEqual(120 - 10 - 60 - 4*(1 + 2) - 3 * 5, game.labs[pl_uuid].money)

    def test_buy_reagents_to_much(self):
        game = Game("test")
        pl_uuid = game.new_lab("test").get_uuid()
        ro_uuid = game.buy_room(pl_uuid)[1].get_uuid()
        eq_uuid = game.buy_equipment(pl_uuid, "auto", "blue", False)[1].get_uuid()
        for x in range(4):
            game.buy_staff(pl_uuid, ro_uuid, "doctor")
            game.buy_staff(pl_uuid, ro_uuid, "lab_assistant")
        game.move_equipment_to_room(pl_uuid, ro_uuid, eq_uuid)
        game.buy_reagents(pl_uuid, eq_uuid, 4)
        pass
        self.assertEqual(0, game.labs[pl_uuid].rooms[ro_uuid].get_equipment().get_reagents())
        self.assertEqual(120 - 10 - 60 - 4 * (1 + 2) - 0 * 5, game.labs[pl_uuid].money)
