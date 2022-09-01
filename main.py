from game.events import events
from game.game import NewGame, GetGame, Game

#
NewGame()
game: Game = GetGame()
# #
pl = game.NewLab("Игрок", "Пароль")
ro = game.BuyRoom(pl.GetUuid())
#
eq = game.BuyEquipment(pl.GetUuid(), ro.GetUuid(), "reporting", None)
# game.BuyPerson(pl.GetUuid(), ro.GetUuid(), "doctor")
# game.BuyPerson(pl.GetUuid(), ro.GetUuid(), "doctor")
# game.BuyPerson(pl.GetUuid(), ro.GetUuid(), "labAssistant")
# game.BuyPerson(pl.GetUuid(), ro.GetUuid(), "labAssistant")
# print("У этого чела репутация:" + str(pl.CalcReputation()))
# print("У этого чела расходы:" + str(pl.CalcExpenses()))
#
# print(copy.copy(game))

events = events()
for x in range(20):
    print(events.GetEvent().GetDescription())
# pickle.dump(game, open("game.pkl", "wb"))
#
# game2 = pickle.load(open("game.pkl", "rb"))
# print(game2)
pass
