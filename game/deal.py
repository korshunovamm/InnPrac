import array
import copy
from uuid import uuid4


class TradeReq:
    def generate_dict(self):
        ret = copy.copy(self.__dict__)
        ret['player0'] = self.player0.get_uuid()
        ret['player1'] = self.player1.get_uuid()
        return ret

    def __init__(self, player_0, player_1, player0_items, player1_items):
        self.uuid = uuid4().hex
        self.player0 = player_0
        self.player1 = player_1
        self.player0_items = player0_items
        self.player1_items = player1_items
        self.status = 'pending'
        self.player0_status = 'accepted'
        self.player1_status = 'pending'
        for item in self.player0_items:
            match item['type']:
                case 'equipment':
                    player_0.get_equipment(item['data']).in_trade = True
                case 'room':
                    player_0.get_room(item['data']).in_trade = True
        for item in self.player0_items:
            match item['type']:
                case 'equipment':
                    player_0.get_equipment(item['data']).in_trade = True
                case 'room':
                    player_0.get_room(item['data']).in_trade = True

    def get_uuid(self):
        return self.uuid

    def accept(self, player):
        if player.get_uuid() == self.player0.get_uuid():
            self.player0_status = 'accepted'
            self.player0 = player
        else:
            self.player1 = player
            self.player1_status = 'accepted'
        if self.can_be_executed():
            self.status = 'executed'
            self.execute()

    def decline(self, player):
        if player.get_uuid() == self.player0.get_uuid():
            self.player0_status = 'declined'
        else:
            self.player1_status = 'declined'

    def can_be_executed(self):
        if not (self.player0_status == 'accepted' and self.player1_status == 'accepted'):
            return False
        for item in self.player0_items:
            money = 0
            match item['type']:
                case 'money':
                    money += item['data']
                    if money > self.player0.money:
                        return False
                case 'equipment':
                    if self.player0.get_equipment(item['data'] is None):
                        return False
                case 'room':
                    if item['data'] not in self.player0.rooms.keys():
                        return False
        for item in self.player1_items:
            money = 0
            match item['type']:
                case 'money':
                    money += item['data']
                    if money > self.player1.money:
                        return False
                case 'equipment':
                    if self.player1.get_equipment(item['data'] is None):
                        return False
                case 'room':
                    if item['data'] not in self.player1.rooms.keys():
                        return False

    def execute(self):
        for item in self.player0_items:
            match item['type']:  # удаляем предметы у первого игрока и добавляем второму
                case 'money':
                    self.player0.buy(item['data'])
                    self.player1.sell(item['data'])
                case 'equipment':
                    self.sell_equipment(item['data'], 0)
                case 'room':
                    self.sell_room(item['data'], 0)
        for item in self.player1_items:
            match item['type']:  # удаляем предметы у второго игрока и добавляем первому
                case 'money':
                    self.player1.buy(item['data'])
                    self.player0.sell(item['data'])
                case 'equipment':
                    self.sell_equipment(item['data'], 1)
                case 'room':
                    self.sell_room(item['data'], 1)

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
        eq.owner = buyer
        buyer.equipments[eq.get_uuid()] = eq

    def sell_room(self, ro_uuid, seller_num):
        seller = self.player0 if seller_num == 0 else self.player1
        buyer = self.player1 if seller_num == 0 else self.player0
        ro = seller.rooms[ro_uuid]
        eq = ro.get_equipment()
        if eq is not None:
            seller.move_equipment_from_room(eq.get_uuid())
        ro.staff_count = {
            'doctor': 0,
            'lab_assistant': 0
        }
        buyer.rooms[ro_uuid] = ro
        del seller.rooms[ro_uuid]


class PledgeReq:
    def generate_dict(self):
        ret = copy.copy(self.__dict__)
        ret['player0'] = self.player0.get_uuid()
        ret['player1'] = self.player1.get_uuid()
        return ret

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
        self.end_date = end_date

    def get_uuid(self):
        return self.uuid

    def get_status(self):
        return self.status

    def accept(self, player) -> tuple[bool, str]:
        if player.get_uuid() == self.player0.get_uuid():
            self.player0 = player
            self.player0_status = 'accepted'
        else:
            self.player1 = player
            player.pledges[self.uuid] = self
            self.player1_status = 'accepted'
        if self.player0_status == 'accepted' and self.player1_status == 'accepted' and self.status == 'pending':
            return self.execute_pledge()
        else:
            return True, "accepted, waiting for another player to accept, or pledge is already executed"

    def decline(self, player):
        if player.get_uuid() == self.player0.get_uuid():
            self.player0_status = 'declined'
        else:
            self.player1_status = 'declined'

    def execute_pledge(self):  # начало, забираем вещи у игрока 0, зачисляем деньги игроку 0
        if self.validate_start():
            self.player1.buy(self.purchase_price)
            self.player0.sell(self.purchase_price)
            for x in self.items:
                match x['type']:
                    case 'equipment':
                        if x['data'].get_uuid() in self.player0.equipments:
                            del self.player0.equipments[x['data'].get_uuid()]
                        else:
                            self.player0.rooms[self.player0.equipment_rooms[x['data'].get_uuid()]].set_eqipment(None)
                    case 'room':
                        x['data'].staff_count = {
                            'doctor': 0,
                            'lab_assistant': 0
                        }
                        eq = x['data'].get_equipment()
                        if eq is not None:
                            self.player0.move_equipment_from_room(eq.get_uuid())
                        del self.player0.rooms[x['data'].get_uuid()]
            self.status = 'executed'
            return True, 'Pledge executed'
        else:
            self.status = 'failed'
            return False, 'some items are not found or not enough money'

    def validate_start(self):
        for x in self.items:
            match x['type']:
                case 'equipment':
                    if self.player0.get_equipment(x['data'].get_uuid()) is None:
                        return False
                case 'room':
                    if x['data'].get_uuid() not in self.player0.rooms:
                        return False
        if self.player1.money < self.purchase_price:
            return False
        return True

    def execute_redeem(self):  # выкупаем предметы назад и зачисляем их на счет игрока 0, деньги на счет игрока 1
        self.status = 'cancelled'
        for x in self.items:
            match x['type']:
                case 'equipment':
                    self.player0.equipments[x['data'].get_uuid()] = x['data']
                case 'room':
                    self.player0.rooms[x['data'].get_uuid()] = x['data']
        self.player0.buy(self.redemption_price)
        self.player1.sell(self.redemption_price)

    def execute_give_bail(self):
        if self.status == 'executed':
            self.status = 'expired'
            del self.player0.pledges[self.uuid]
            del self.player1.pledges[self.uuid]
            for x in self.items:
                match x['type']:
                    case 'equipment':
                        x['data'].owner = self.player1.get_uuid()
                        self.player1.equipments[x['data'].get_uuid()] = x['data']
                    case 'room':
                        self.player1.rooms[x['data'].get_uuid()] = x['data']


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
                        self.player.move_equipment_from_room(x['data'].get_equipment().get_uuid())
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
            self.status = 'canceled'
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
        self.price: int = 0
        self.status = 'waiting'
        self.pl_0_status: str = 'accepted'
        self.pl_1_status: str = 'waiting'
        player_0.power_sells[self.uuid] = self
        player_1.power_sells[self.uuid] = self

    def accept(self, pl):
        if pl == self.player_0:
            self.pl_0_status = 'accepted'
        elif pl == self.player_1:
            self.pl_1_status = 'accepted'
        if self.pl_0_status == 'accepted' and self.pl_1_status == 'accepted':
            return self.execute()

    def execute(self):
        if self.status != 'waiting':
            return False, "Already executed, cancelled or rejected"
        can_execute = self.check_logistic()
        if not can_execute:
            return False, "Can't execute. Problems with logistic"
        for x in self.items:
            eq = self.player_0.get_equipment(x['eq_uuid'])
            if eq is None or eq.get_power() < x['amount']:
                can_execute = False
        if can_execute:
            for x in self.items:
                eq = self.player_0.get_equipment(x['eq_uuid'])
                self.player_1.my_power.append({
                    'pl_uuid': eq.owner,
                    'type': eq.get_type(),
                    'amount': x['amount']
                })
                eq.sell_power(self.player_1.get_uuid(), x['amount'])
            self.player_0.sell(self.price)
            self.player_1.buy(self.price)
            self.status = 'executed'
            return True, None
        return False
        # self.player_0.buy(self.price)
        # self.player_1.sell(self.price)
        # del self.player_0.power_sells[self.uuid]
        # del self.player_1.power_sells[self.uuid]
        # return True

    def check_logistic(self) -> bool:
        if self.player_0.services['logistic'] or self.player_1.services['logistic']:
            if self.player_0.events['need_have_logistic'] and not self.player_0.services['logistic'] or \
                    self.player_0.events['need_have_logistic'] and not self.player_0.services['logistic']:
                return False
            return True
        return False
