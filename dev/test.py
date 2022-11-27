from game.deal import TradeReq, PledgeReq
from game.entitys.equipment import Equipment
import xlsxwriter
from game.entitys.events import Events, Event
from game.entitys.order import Order
from game.entitys.room import Room
from game.game import Game
from game.player import Player

pl = Player("test")
pl2 = Player("test")
expenses = []
obj = PledgeReq(pl, pl2, 0, 0, [], 2)
dict_ = obj.generate_dict()
workbook = xlsxwriter.Workbook('dev/' + str(type(obj)).split(".")[-1][:-2]+'.xlsx')
worksheet = workbook.add_worksheet()

for x in dict_:
    if x != "uuid":
        expenses.append([x, str(dict_[x]), str(type(obj.__dict__[x])).split(".")[-1][:-2].replace("<class '", "")])

expenses = tuple(expenses)
row, col = 0, 0
for item, defLoc, typeO in expenses:
    worksheet.write(row, col, item)
    worksheet.write(row, col + 2, defLoc)
    worksheet.write(row, col + 3, typeO)
    row += 1

workbook.close()
