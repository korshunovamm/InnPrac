from game.game import NewGame, GetGame, Game

NewGame()
game: Game = GetGame()
#
pl = game.NewLab("Игрок", "Пароль")
ro = game.BuyRoom(pl.GetUuid())

eq = game.BuyEquipment(pl.GetUuid(), ro.GetUuid(), "hand", "yellow")
game.BuyPerson(pl.GetUuid(), ro.GetUuid(), "doctor")
game.BuyPerson(pl.GetUuid(), ro.GetUuid(), "doctor")
game.BuyPerson(pl.GetUuid(), ro.GetUuid(), "labAssistant")
game.BuyPerson(pl.GetUuid(), ro.GetUuid(), "labAssistant")
print("У этого чела репутация:" + str(pl.CalcReputation()))
print("У этого чела расходы:" + str(pl.CalcExpenses()))
#
# pickle.dump(game, open("game.pkl", "wb"))
#
# game2 = pickle.load(open("game.pkl", "rb"))
# print(game2)
pass
