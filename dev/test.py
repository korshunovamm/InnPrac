from game.entitys.equipment import Equipment
import xlsxwriter
from game.entitys.events import Events, Event
from game.entitys.order import Order
from game.entitys.room import Room
from game.game import Game
from game.player import Player

workbook = xlsxwriter.Workbook('dev/test.xlsx')
worksheet = workbook.add_worksheet()
pl = Player("test")
expenses = []
obj = Order("yellow", pl).generate_dict()
for x in obj:
    if x != "uuid":
        expenses.append([x, str(obj[x]), str(type(obj[x]))[len("<class '"):-len("'>")]])

expenses = tuple(expenses)
row, col = 0, 0
for item, defLoc, typeO in expenses:
    worksheet.write(row, col, item)
    worksheet.write(row, col + 2, defLoc)
    worksheet.write(row, col + 3, typeO)
    row += 1

workbook.close()
