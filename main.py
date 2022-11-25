# import os
# abspath = os.path.abspath(__file__)
# dname = os.path.dirname(abspath)
# os.chdir(dname)
# import asyncio
# from server.server_start import main
# asyncio.run(main())
from game.game import Game

game = Game("test")
pl = game.new_lab("test")
eq = game.buy_equipment(pl.get_uuid(), "hand", "yellow", False)[1]
ro = game.buy_room(pl.get_uuid())[1]
pl.move_equipment_to_room(eq.get_uuid(), ro.get_uuid())
for x in range(4):
    game.buy_staff(pl.get_uuid(), ro.get_uuid(), "doctor")
    game.buy_staff(pl.get_uuid(), ro.get_uuid(), "lab_assistant")
game.buy_reagents(pl.get_uuid(), eq.get_uuid(), 1)
pl.orders_input["yellow"] = True
pl.pay_type = "pre_pay"
game.transition_to_stage_2()
game.transition_to_stage_1()
pass
