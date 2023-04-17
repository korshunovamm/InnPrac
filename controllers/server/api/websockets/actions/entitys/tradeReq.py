def new(websocket, data):
    game = websocket.game
    if not data['pl_1_uuid'] in game.labs or not type(data['pl_0_items']) == list or\
            not type(data['pl_1_items']) == list:
        return dict(result="error", message="Invalid data")
    pl_0 = game.labs[websocket.pl_uuid]
    pl_1 = game.labs[data['pl_1_uuid']]
    if len(data['pl_0_items']) + len(data['pl_1_items']) == 0:
        return dict(result="error", message="Invalid data")
    if websocket.pl_uuid == data['pl_1_uuid']:
        return dict(result="error", message="Invalid data")
    money = 0
    for x in data['pl_0_items']:
        match x['type']:
            case "room":
                if not x['data'] in pl_0.rooms:
                    return dict(result="error", message="Invalid data")
            case "equipment":
                if not pl_0.get_equipment(x['data']):
                    return dict(result="error", message="Invalid data")
            case "money":
                if not type(x['data']) == int:
                    return dict(result="error", message="Invalid data")
                money += x["data"]
            case _:
                return dict(result="error", message="Invalid data")
    if money > pl_0.money:
        return dict(result="error", message="Invalid data")
    money = 0
    for x in data['pl_1_items']:
        match x['type']:
            case "room":
                if not x['data'] in pl_1.rooms:
                    return dict(result="error", message="Invalid data")
            case "equipment":
                if not pl_1.get_equipment(x['data']):
                    return dict(result="error", message="Invalid data")
            case "money":
                if not type(x['data']) == int:
                    return dict(result="error", message="Invalid data")
                money += x["data"]
            case _:
                return dict(result="error", message="Invalid data")
    if money > pl_1.money:
        return dict(result="error", message="Invalid data")
    trade = game.new_trade_req(websocket.pl_uuid, data["pl_1_uuid"], data["pl_0_items"], data["pl_1_items"])
    if trade[0]:
        return dict(result="ok", message="Trade request sent", data=trade[1].generate_dict())
    else:
        return dict(result="error", message="Trade request not sent")


def accept(websocket, data):
    game = websocket.game
    pl = game.labs[websocket.pl_uuid]
    if not data['tr_uuid'] in pl.trade_requests:
        return dict(result="error", message="Invalid data")
    trade = pl.trade_requests[data['tr_uuid']]
    if trade.status != "pending":
        return dict(result="error", message="Already executed/failed")
    if trade.pl0.get_uuid() == websocket.pl_uuid:
        if trade.pl0_status == "accepted":
            return dict(result="error", message="Already accepted")
    elif trade.pl1.get_uuid() == websocket.pl_uuid:
        if trade.pl1_status == "accepted":
            return dict(result="error", message="Already accepted")
    else:
        return dict(result="error", message="Invalid data")
    res = trade.accept(pl)
    if res[0]:
        return dict(result="ok", message=res[1], data=trade.generate_dict())
    else:
        return dict(result="error", message=res[1])
