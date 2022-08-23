from game.game import Game
from game.player import Player

game = Game()


def GetGame():
    return game


pl = game.NewLab("Игрок", "Пароль")
pl.CalcOrdersCount(4)
print(pl.GetOrders())
