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
    def __init__(self, player_0, price, player1_item):
        self.uuid = uuid4().hex
        self.player0 = player_0
        self.player1 = None
        self.player0_money = player0_money
        self.player1_items = player1_item
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

    # def execute(self):

