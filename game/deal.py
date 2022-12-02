import array
import copy
from uuid import uuid4


class TradeReq:
    def generate_dict(self):
        ret = copy.copy(self.__dict__)
        ret['pl0'] = self.pl0.get_uuid()
        ret['pl1'] = self.pl1.get_uuid()
        return ret

    def __init__(self, player_0, player_1, pl0_items, pl1_items):
        self.uuid = uuid4().hex
        self.pl0 = player_0
        self.pl1 = player_1
        self.pl0_items = pl0_items
        self.pl1_items = pl1_items
        self.status = 'pending'
        self.pl0_status = 'accepted'
        self.pl1_status = 'declined'

    def get_uuid(self):
        return self.uuid

    def accept(self, player):
        if player.get_uuid() == self.pl0.get_uuid():
            self.pl0_status = 'accepted'
            self.pl0 = player
        else:
            self.pl1 = player
            self.pl1_status = 'accepted'
        if self.pl0_status == 'accepted' and self.pl1_status == 'accepted':
            return True, "Accepted, " +  self.execute()
        return True, "Accepted, dont't execute"

    def decline(self, player):
        if player.get_uuid() == self.pl0.get_uuid():
            self.pl0_status = 'declined'
        else:
            self.pl1_status = 'declined'

    def can_execute(self):
        if not (self.pl0_status == 'accepted' and self.pl1_status == 'accepted'):
            return False
        money = 0
        for x in self.pl0_items:
            match x['type']:
                case "room":
                    if not x['data'] in self.pl0.rooms:
                        return False
                case "equipment":
                    if not self.pl0.get_equipment(x['data']):
                        return False
                case "money":
                    money = x['data']
                case _:
                    return False
        if self.pl0.money < money:
            return False
        money = 0
        for x in self.pl1_items:
            match x['type']:
                case "room":
                    if not x['data'] in self.pl1.rooms:
                        return False
                case "equipment":
                    if not self.pl1.get_equipment(x['data']):
                        return False
                case "money":
                    money = x['data']
                case _:
                    return False
        if self.pl1.money < money:
            return False
        return True

    def execute(self):
        if not self.can_execute():
            self.status = 'failed'
            return "Failed"
        self.status = 'executed'
        for item in self.pl0_items:
            match item['type']:  # удаляем предметы у первого игрока и добавляем второму
                case 'money':
                    self.pl0.buy(item['data'])
                    self.pl1.sell(item['data'])
                case 'equipment':
                    self.sell_equipment(item['data'], 0)
                case 'room':
                    self.sell_room(item['data'], 0)
        for item in self.pl1_items:
            match item['type']:  # удаляем предметы у второго игрока и добавляем первому
                case 'money':
                    self.pl1.buy(item['data'])
                    self.pl0.sell(item['data'])
                case 'equipment':
                    self.sell_equipment(item['data'], 1)
                case 'room':
                    self.sell_room(item['data'], 1)
        return "Executed"

    def sell_equipment(self, eq_uuid, seller_num):
        seller = self.pl0 if seller_num == 0 else self.pl1
        buyer = self.pl1 if seller_num == 0 else self.pl0
        if eq_uuid in seller.equipments.keys():
            eq = seller.equipments[eq_uuid]
            del seller.equipments[eq_uuid]
        else:
            eq = seller.rooms[seller.equipments_rooms[eq_uuid]].get_equipment()
            seller.rooms[seller.equipments_rooms[eq_uuid]].set_equipment(None)
            del seller.equipments_rooms[eq_uuid]
        eq.owner = buyer
        buyer.equipments[eq.get_uuid()] = eq

    def sell_room(self, ro_uuid, seller_num):
        seller = self.pl0 if seller_num == 0 else self.pl1
        buyer = self.pl1 if seller_num == 0 else self.pl0
        ro = seller.rooms[ro_uuid]
        eq = ro.get_equipment()
        if eq is not None:
            seller.move_equipment_from_room(ro.get_uuid())
        ro.staff_count = {
            'doctor': 0,
            'lab_assistant': 0
        }
        buyer.rooms[ro_uuid] = ro
        del seller.rooms[ro_uuid]


class PledgeReq:
    def generate_dict(self):
        ret = copy.copy(self.__dict__)
        ret['pl0'] = self.pl0.get_uuid()
        ret['pl1'] = self.pl1.get_uuid()
        return ret

    def __init__(self, player_0, player_1, purchase_price: int, redemption_price: int, items: array, end_month: int):
        self.uuid = uuid4().hex
        self.pl0 = player_0
        self.pl1 = player_1
        player_0.pledges[self.uuid] = self
        player_1.pledges[self.uuid] = self
        self.purchase_price = purchase_price
        self.redemption_price = redemption_price
        self.items = items
        self.status = 'pending'
        self.pl0_status = 'accepted'
        self.pl0.pledges[self.uuid] = self
        self.pl1_status = 'canceled'
        self.end_month = end_month

    def get_uuid(self):
        return self.uuid

    def get_status(self):
        return self.status

    def accept(self, player) -> tuple[bool, str]:
        if player.get_uuid() == self.pl0.get_uuid():
            self.pl0 = player
            self.pl0_status = 'accepted'
        else:
            self.pl1 = player
            player.pledges[self.uuid] = self
            self.pl1_status = 'accepted'
        if self.pl0_status == 'accepted' and self.pl1_status == 'accepted' and self.status == 'pending':
            return self.execute_pledge()
        else:
            return True, "accepted, waiting for another player to accept, or pledge is already executed"

    def decline(self, player):
        if player.get_uuid() == self.pl0.get_uuid():
            self.pl0_status = 'canceled'
        else:
            self.pl1_status = 'canceled'

    def execute_pledge(self):  # начало, забираем вещи у игрока 0, зачисляем деньги игроку 0
        if self.validate_start():
            self.pl1.buy(self.purchase_price)
            self.pl0.sell(self.purchase_price)
            for x in self.items:
                match x['type']:
                    case 'equipment':
                        if x['data'].get_uuid() in self.pl0.equipments:
                            del self.pl0.equipments[x['data'].get_uuid()]
                        else:
                            self.pl0.rooms[self.pl0.equipment_rooms[x['data'].get_uuid()]].set_eqipment(None)
                    case 'room':
                        x['data'].staff_count = {
                            'doctor': 0,
                            'lab_assistant': 0
                        }
                        eq = x['data'].get_equipment()
                        if eq is not None:
                            self.pl0.move_equipment_from_room(x['data'].get_uuid())
                        del self.pl0.rooms[x['data'].get_uuid()]
            self.status = 'executed'
            return True, 'Pledge executed'
        else:
            self.status = 'failed'
            return False, 'some items are not found or not enough money'

    def validate_start(self):
        for x in self.items:
            match x['type']:
                case 'equipment':
                    if self.pl0.get_equipment(x['data'].get_uuid()) is None:
                        return False
                case 'room':
                    if x['data'].get_uuid() not in self.pl0.rooms:
                        return False
        if self.pl1.money < self.purchase_price:
            return False
        return True

    def execute_redeem(self):  # выкупаем предметы назад и зачисляем их на счет игрока 0, деньги на счет игрока 1
        self.status = 'cancelled'
        for x in self.items:
            match x['type']:
                case 'equipment':
                    self.pl0.equipments[x['data'].get_uuid()] = x['data']
                case 'room':
                    self.pl0.rooms[x['data'].get_uuid()] = x['data']
        self.pl0.buy(self.redemption_price)
        self.pl1.sell(self.redemption_price)

    def execute_give_bail(self):
        if self.status == 'executed':
            self.status = 'expired'
            del self.pl0.pledges[self.uuid]
            del self.pl1.pledges[self.uuid]
            for x in self.items:
                match x['type']:
                    case 'equipment':
                        x['data'].owner = self.pl1.get_uuid()
                        self.pl1.equipments[x['data'].get_uuid()] = x['data']
                    case 'room':
                        self.pl1.rooms[x['data'].get_uuid()] = x['data']


class PledgeBank:
    def generate_dict(self):
        ret = copy.copy(self.__dict__)
        ret['player'] = self.player.get_uuid()
        ret['items'] = []
        for x in self.items:
            ret['items'].append({
                'type': x['type'],
                'data': x['data'].get_uuid()
            })
        return ret

    def __init__(self, player, items):
        self.uuid = uuid4().hex
        self.player = player
        self.items = items
        self.price = 0
        for x in self.items:
            match x['type']:
                case 'equipment':
                    eq = self.player.get_equipment(x['data'])
                    if x['data'] in self.player.equipments:
                        del self.player.equipments[x['data']]
                    else:
                        del self.player.equipments_rooms[x['data']]
                    x['data'] = eq
                case 'room':
                    x['data'] = self.player.rooms[x['data']]
                    if x['data'].get_equipment() is not None:
                        self.player.move_equipment_from_room(x['data'].get_uuid())
                    del self.player.rooms[x['data'].get_uuid()]
                    x['data'].staff_count = {
                        'doctor': 0,
                        'lab_assistant': 0
                    }
            player.bank_pledges[self.uuid] = self
            self.price += int(round(x['data'].get_price() / 2))
        self.status = 'in_bank'

    def get_uuid(self):
        return self.uuid

    def get_status(self):
        return self.status

    def purchase(self):
        if self.player.get_money() > self.price and self.status == 'in_bank':
            self.player.buy(self.price)
            for x in self.items:
                match x['type']:
                    case 'equipment':
                        self.player.equipments[x['data'].get_uuid()] = x['data']
                    case 'room':
                        self.player.rooms[x['data'].get_uuid()] = x['data']
            self.status = 'redeemed'
            return True, self
        else:
            return False, None


class PowerSell:
    def generate_dict(self):
        ret = copy.copy(self.__dict__)
        ret['player_0'] = self.player_0.get_uuid()
        ret['player_1'] = self.player_1.get_uuid()
        ret['items'] = []
        for x in self.items:
            ret['items'].append(dict(type=x['type'], eq_uuid=x['eq_uuid']))
        return ret

    def __init__(self, player_0, player_1, items, price):
        self.uuid: str = uuid4().hex
        self.player_0 = player_0
        self.player_1 = player_1
        self.items: list[dict] = items
        self.price: int = price
        self.status = 'waiting'
        self.pl0_status: str = 'accepted'
        self.pl1_status: str = 'canceled'
        player_0.power_sells[self.uuid] = self
        player_1.power_sells[self.uuid] = self

    def cancel(self, pl):
        if self.status == 'waiting':
            if self.player_0.get_uuid() == pl.get_uuid():
                self.pl0_status = 'canceled'
                return True
            elif self.player_1.get_uuid() == pl.get_uuid():
                self.pl1_status = 'canceled'
                return True
            else:
                return False
        else:
            return False

    def accept(self, pl):
        if pl == self.player_0:
            self.pl0_status = 'accepted'
        elif pl == self.player_1:
            self.pl1_status = 'accepted'
        if self.pl0_status == 'accepted' and self.pl1_status == 'accepted':
            return self.execute()

    def execute(self):
        if self.status != 'waiting':
            self.status = 'failed'
            return False, "Already executed, cancelled or failed"
        can_execute = self.check_logistic()
        if not can_execute:
            self.status = 'failed'
            return False, "Can't execute. Problems with logistic"
        for x in self.items:
            eq = self.player_0.get_equipment(x['eq_uuid'])
            if eq is None or eq.get_power() < x['amount']:
                can_execute = False
        if can_execute:
            for x in self.items:
                eq = self.player_0.get_equipment(x['eq_uuid'])
                if eq.get_type() not in ["auto", "semi_manual", "hand"]:
                    self.player_1.my_power.append({
                        'pl_uuid': eq.owner,
                        'type': eq.get_type(),
                        'amount': x['amount']
                    })
                else:
                    self.player_1.my_power.append({
                        'pl_uuid': eq.owner,
                        'type': eq.get_type(),
                        'color': eq.get_color(),
                        'amount': x['amount']
                    })
                eq.sell_power(self.player_1.get_uuid(), x['amount'])
            self.player_0.sell(self.price)
            self.player_1.buy(self.price)
            self.status = 'executed'
            return True, None
        else:
            self.status = 'failed'
            return False, "Can't execute. Dont have enough power"

    def check_logistic(self) -> bool:
        if self.player_0.services['logistic'] or self.player_1.services['logistic']:
            if self.player_0.events['need_have_logistic'] and not self.player_0.services['logistic'] or \
                    self.player_0.events['need_have_logistic'] and not self.player_0.services['logistic']:
                return False
            return True
        return False
