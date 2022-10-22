from game.deal import PowerSell
from game.entitys.events import Events
from game.game import Game

# fullgame.main()
game: Game = Game("test")
pl = game.new_lab("test")
pl2 = game.new_lab("test")
ro = game.buy_room(pl.get_uuid())[1]
eq = game.buy_equipment(pl.get_uuid(), "auto", "red", True)[1]
for x in range(4):
    game.buy_staff(pl.get_uuid(), ro.get_uuid(), "lab_assistant")
    game.buy_staff(pl.get_uuid(), ro.get_uuid(), "doctor")

pl.set_orders_input({
    'yellow': True,
    'red': True,
    'blue': True,
    'green': True,
    'purple': True,
    'grey': True
})
for x in range(4):
    game.buy_staff(pl.get_uuid(), ro.get_uuid(), "doctor")
    game.buy_staff(pl.get_uuid(), ro.get_uuid(), "lab_assistant")
game.move_equipment_to_room(pl.get_uuid(), ro.get_uuid(), eq.get_uuid())
game.buy_reagents(pl.get_uuid(), eq.get_uuid(), 4)
power_sell = PowerSell(pl, pl2, [{
    'eq_uuid': eq.get_uuid(),
    'amount': 1
}], 5)
game.transition_to_stage_2()
pl.buy_logistic_service()
# power_sell.accept(pl2)
pass
