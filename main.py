from game.entitys.events import Events
from game.game import Game

# fullgame.main()
game: Game = Game("test")
pl = game.new_lab("test")
ro = game.buy_room(pl.get_uuid())[1]
eq = game.buy_equipment(pl.get_uuid(), "auto", "red", True)[1]
pl.set_orders_input({
    'yellow': False,
    'red': True,
    'blue': False,
    'green': False,
    'purple': True,
    'grey': False
})
game.move_equipment_to_room(pl.get_uuid(), ro.get_uuid(), eq.get_uuid())
for x in range(4):
    game.buy_staff(pl.get_uuid(), ro.get_uuid(), "doctor")
    game.buy_staff(pl.get_uuid(), ro.get_uuid(), "lab_assistant")
game.transition_to_stage_2()
pass
