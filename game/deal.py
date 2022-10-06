import array
from uuid import uuid4


class TradeReq:
    def __init__(self, player_0, player0_items, player1_items):
        self.uuid = uuid4().hex
        self.player0 = player_0
        self.player1 = None
        self.player0_items = player0_items
        self.player1_items = player1_items
        self.status = 'pending'
        self.player0_status = 'accepted'
        self.player1_status = 'pending'

    def get_uuid(self):
        return self.uuid

    def accept(self, player):
        if player.get_uuid() == self.player0.get_uuid():
            self.player0_status = 'accepted'
            self.player0 = player
        else:
            self.player1 = player
            self.player1_status = 'accepted'
        if self.player0_status == 'accepted' and self.player1_status == 'accepted':
            self.status = 'executed'
            self.execute()

    def decline(self, player):
        if player.get_uuid() == self.player0.get_uuid():
            self.player0_status = 'declined'
        else:
            self.player1_status = 'declined'

    def execute(self):
        for item in self.player0_items:
            match item["type"]: # удаляем предметы у первого игрока и добавляем второму
                case "money":
                    self.player0.buy(item["data"])
                    self.player1.sell(item["data"])
                case "equipment":
                    self.sell_equipment(item["data"], 0)
                case "room":
                    self.sell_room(item["data"], 0)

        for item in self.player1_items:
            match item["type"]:  # удаляем предметы у второго игрока и добавляем первому
                case "money":
                    self.player1.buy(item["data"])
                    self.player0.sell(item["data"])
                case "equipment":
                    self.sell_equipment(item["data"], 1)
                case "room":
                    self.sell_room(item["data"], 1)

    def sell_equipment(self, eq_uuid, seller_num):
        seller = self.player0 if seller_num == 0 else self.player1
        buyer = self.player1 if seller_num == 0 else self.player0
        if eq_uuid in seller.equipments.keys():
            eq = seller.equipments[eq_uuid]
            del seller.equipments[eq_uuid]
        else:
            eq = seller.rooms[seller.equipments_rooms[eq_uuid]].get_equipment()
            seller.rooms[seller.equipments_rooms[eq_uuid]].set_equipment(None)
            del seller.equipments_rooms[eq_uuid]
        buyer.equipments[eq.get_uuid()] = eq

    def sell_room(self, ro_uuid, seller_num):
        seller = self.player0 if seller_num == 0 else self.player1
        buyer = self.player1 if seller_num == 0 else self.player0
        ro = seller.rooms[ro_uuid]
        eq = ro.get_equipment()
        if eq is not None:
            seller.move_equipment_from_room(eq.get_uuid())
        ro.staff_count = {
            "doctor": 0,
            "lab_assistant": 0
        }
        buyer.rooms[ro_uuid] = ro
        del seller.rooms[ro_uuid]

class PledgeReq:
    def __init__(self, player_0, purchase_price: int, redemption_price: int, items: array, end_date: int):
        self.uuid = uuid4().hex
        self.player0 = player_0
        self.player1 = None
        self.purchase_price = purchase_price
        self.redemption_price = redemption_price
        self.items = items
        self.status = 'pending'
        self.player0_status = 'accepted'
        self.player0.pledges[self.uuid] = self
        self.player1_status = 'pending'


    def get_uuid(self):
        return self.uuid

    def get_status(self):
        return self.status
    def accept(self, player):
        if player.get_uuid() == self.player0.get_uuid():
            self.player0 = player
            self.player0_status = 'accepted'
        else:
            self.player1 = player
            player.pledges[self.uuid] = self
            self.player1_status = 'accepted'
        if self.player0_status == 'accepted' and self.player1_status == 'accepted' and self.status == 'pending':
            self.status = 'executed'
            self.execute_pledge()

    def decline(self, player):
        if player.get_uuid() == self.player0.get_uuid():
            self.player0_status = 'declined'
        else:
            self.player1_status = 'declined'

    def execute_pledge(self): # TODO: начало, забираем вещи у игрока 0, зачисляем деньги игроку 0
        self.player1.buy(self.purchase_price)
        self.player0.sell(self.purchase_price)
        for x in self.items:
            match x["type"]:
                case "equipment":
                    self.player1.equipments[x["data"].get_uuid()] = x["data"]
                case "room":
                    x["data"].staff_count = {
                        "doctor": 0,
                        "lab_assistant": 0
                    }
                    eq = x["data"].get_equipment()
                    if eq is not None:
                        self.player0.move_equipment_from_room(eq.get_uuid())
                    del self.player0.rooms[x["data"].get_uuid()]
        pass # TODO: продаем предметы игроку 1 и получаем деньги на счет игрока 0

    def execute_redeem(self): # TODO: выкупаем предметы назад и зачисляем их на счет игрока 0, деньги на счет игрока 1
        self.status = 'cancelled'
        for x in self.items:
            match x["type"]:
                case "equipment":
                    self.player0.equipments[x["data"].get_uuid()] = x["data"]
                case "room":
                    self.player0.rooms[x["data"].get_uuid()] = x["data"]
        self.player0.buy(self.redemption_price)
        self.player1.sell(self.redemption_price)

    def execute_give_bail(self):
        if self.status == 'executed':
            del self.player0.pledges[self.uuid]
            del self.player1.pledges[self.uuid]
            for x in self.items:
                match x["type"]:
                    case "equipment":
                        self.player1.equipments[x["data"].get_uuid()] = x["data"]
                    case "room":
                        self.player1.rooms[x["data"].get_uuid()] = x["data"]