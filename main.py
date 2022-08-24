import pickle

from game.game import Game

game = Game()



pl = game.NewLab("Игрок", "Пароль")
ro = pl.buyRoom()

game.BuyEquipment(pl.GetUuid(), ro.GetUuid(), "semi-manual", "yellow")

print(ro.GetEquipment())
print(game._equipments)
# pickle.dump(game, open("game.pkl", "wb"))
#
# game2 = pickle.load(open("game.pkl", "rb"))
# print(game2)
