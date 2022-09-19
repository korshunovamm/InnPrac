from game.game import GetGame, NewGame, Game

# fullgame.main()
NewGame()
game: Game = GetGame()
pl = game.NewLab("Игрок", "Пароль")
ro = game.BuyRoom(pl.GetUuid())
game.BuyPerson(pl.GetUuid(), ro.GetUuid(), "doctor")
pass
game.SellPerson(pl.GetUuid(), ro.GetUuid(), "doctor")
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
