from game.game import Game

game = Game()
user = game.NewLab("test", "test")
# orders = user.CalcOrdersCount(4)

#
pl = game.NewLab("Игрок", "Пароль")
roo = pl.BuyRoom()
game.BuyEquipment(pl.GetUuid(), roo.GetUuid(), "hand", "yellow")
game.BuyPerson(pl.GetUuid(), roo.GetUuid(), "doctor")
game.BuyPerson(pl.GetUuid(), roo.GetUuid(), "labAssistant")
print(pl.CalcReputation())
# game.BuyEquipment(pl.GetUuid(), ro.GetUuid(), "semi-manual", "yellow")
#
# print(ro.GetEquipment())
# print(game._equipments)
# pickle.dump(game, open("game.pkl", "wb"))
#
# game2 = pickle.load(open("game.pkl", "rb"))
# print(game2)
pass
