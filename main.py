from game.deal import PledgeBank
from game.entitys.events import Events
from game.game import Game

# fullgame.main()
game: Game = Game()
pl = game.new_lab()
ro = game.buy_room(pl.get_uuid())[1]
eq = game.buy_equipment(pl.get_uuid(), "auto", "yellow", True)[1]
# game.move_equipment_to_room(pl.get_uuid(), ro.get_uuid(), eq.get_uuid())
# pledge = PledgeBank(pl, [{"type": "room", "data": ro.get_uuid()}, {"type": "equipment", "data": eq.get_uuid()}])
# # trade = TradeReq(pl2, [{"type": "equipment", "data": eq2.get_uuid()}, {"type": "room", "data": ro2.get_uuid()}],
# # [{"type":| "money", "data": 5}]) trade.accept(pl)
ev = Events()
pass
