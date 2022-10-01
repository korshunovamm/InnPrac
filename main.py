from game.game import Game

# fullgame.main()
game: Game = Game()
pl = game.new_lab("Игрок", "Пароль")
ro = game.buy_room(pl.get_uuid())
game.buy_equipment(pl.get_uuid(), "auto", "yellow", True)
print(game.buy_equipment(pl.get_uuid(), "auto", "yellow", True))
# ro2 = game.BuyRoom(pl.GetUuid())
# game.BuyPerson(pl.GetUuid(), ro.GetUuid(), "doctor")
pass
# pl.SetOrdersInput({'yellow': True, 'red': False, 'blue': False, 'green': False, 'purple': False, 'grey': False})
# ro = game.BuyRoom(pl.GetUuid())
# game.BuyEquipment(pl.GetUuid(), ro.GetUuid(), "reporting", None, True)
# game.BuyLIS(pl.GetUuid(), ro.GetUuid())
# pl.GetPowerUnits()
# power = pl.GetPowerUnits()
# anal = PowerUnit("analytic", "yellow", pl.GetUuid(), ro.GetUuid())
# preanal = PowerUnit("preanalytic", "yellow", pl.GetUuid(), ro.GetUuid())

pass
