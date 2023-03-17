from engine.deal import TradeReq, PledgeReq, PowerSell
from engine.entitys.equipment import Equipment
import xlsxwriter
from engine.entitys.events import Events, Event
from engine.entitys.order import Order
from engine.entitys.room import Room
from engine.deal import PledgeBank
from engine.game import Game
from engine.player import Player

pl = Player("test")
pl2 = Player("test")
eq = pl.buy_equipment("auto", "yellow")
expenses = []
obj = PledgeBank(pl, [{"type": "equipment", "data": eq.get_uuid()}])
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
