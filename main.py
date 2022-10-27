from game.deal import PowerSell, PledgeReq
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
pledge = game.new_pledge_req(pl.get_uuid(), pl2.get_uuid(), 1, 2, [
    {
        'type': 'room',
        'data': ro
    },
    {
        'type': 'equipment',
        'data': eq
    }
], 1)
pl2.pledges[pledge[1].get_uuid()].accept(pl2)
game.transition_to_stage_2()
game.transition_to_stage_1()
game.transition_to_stage_2()
game.transition_to_stage_1()
# power_sell.accept(pl2)
pass
