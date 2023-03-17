from engine.deal import PledgeBank, PledgeReq


def buy_logistic_service(websocket, data):
    if websocket.game.stage == 1:
        res = websocket.game.labs[websocket.pl_uuid].buy_logistic_service()
        if res:
            return {"result": "ok", "message": "", "data": websocket.game.labs[websocket.pl_uuid].services}
        return {"result": "error", "message": "You can't buy logistic service"}
    return {"result": "error", "message": "You can't buy logistic service"}


def buy_training_service(websocket, data):
    if websocket.game.stage == 1:
        res = websocket.game.labs[websocket.pl_uuid].buy_training_service()
        if res:
            return {"result": "ok", "message": "", "data": websocket.game.labs[websocket.pl_uuid].services}
        return {"result": "error", "message": "You can't buy training service"}
    return {"result": "error", "message": "You can't buy training service"}


def new_bank_deposit(websocket, data):
    if websocket.game.stage == 1:
        if not isinstance(data.get("items"), list):
            return {"result": "error", "message": "Invalid data"}
        if len(data["items"]) <= 0:
            return {"result": "error", "message": "You can't deposit nothing"}
        for x in data["items"]:
            if not isinstance(x, dict):
                return {"result": "error", "message": "Invalid data"}
            if x.get("type") == "room":
                if not websocket.game.labs[websocket.pl_uuid].rooms.get(x.get("data")):
                    return {"result": "error", "message": "Invalid data"}
            elif x.get("type") == "equipment":
                if not websocket.game.labs[websocket.pl_uuid].get_equipment(x.get("data")):
                    return {"result": "error", "message": "Invalid data"}
            else:
                return {"result": "error", "message": "Invalid data"}
        if websocket.game.stage != 1:
            return {"result": "error", "message": "You can't deposit items"}
        pledge = PledgeBank(websocket.game.labs[websocket.pl_uuid], data["items"])
        return {"result": "ok", "message": "Pledge accepted", "data": pledge.generate_dict()}
    return {"result": "error", "message": "You can't pledge with bank"}


def redeem_bank_deposit(websocket, data):
    if data["plg_uuid"] in websocket.game.labs[websocket.pl_uuid].pledges:
        plg = websocket.game.get_pledge(data.get("plg_uuid"))
    elif data["plg_uuid"] in websocket.game.labs[websocket.pl_uuid].bank_pledges:
        plg = websocket.game.labs[websocket.pl_uuid].bank_pledges[data.get("plg_uuid")]
    else:
        return {"result": "error", "message": "Invalid data"}
    if websocket.game.stage == 1:
        if plg.player.get_uuid() == websocket.pl_uuid and plg.get_status() == "in_bank":
            res = plg.purchase()
            if res[0]:
                return {"result": "ok", "message": "Pledge redeemed", "data": res[1].generate_dict()}
            return {"result": "error", "message": "Pledge not redeemed"}
        return {"result": "error", "message": "You can't redeem this pledge"}
    return {"result": "error", "message": "You can't redeem pledge"}


def new_deal(websocket, data):
    if not isinstance(data.get("my_items"), list) or not isinstance(data.get("partner_items"), list):
        return {"result": "error", "message": "Invalid data"}
    if len(data["items"]) <= 0 and len(data["partner_items"]) <= 0:
        return {"result": "error", "message": "You can't pledge nothing"}
    for x in data["items"]:
        if not isinstance(x, dict):
            return {"result": "error", "message": "Invalid data"}
        if x.get("type") == "room":
            if not websocket.game.labs[websocket.pl_uuid].rooms.get(x.get("data")):
                return {"result": "error", "message": "Invalid data"}
        elif x.get("type") == "equipment":
            if not websocket.game.labs[websocket.pl_uuid].get_equipment(x.get("data")):
                return {"result": "error", "message": "Invalid data"}
        elif x.get("type") == "money":
            if not isinstance(x.get("data"), int):
                return {"result": "error", "message": "Invalid data"}
        else:
            return {"result": "error", "message": "Invalid data"}
    if websocket.game.stage != 1:
        return {"result": "error", "message": "You can't create deal"}
    pledge = PledgeReq(websocket.game.labs[websocket.pl_uuid], ) # TODO: fix this
    return {"result": "ok", "message": "Pledge accepted", "data": pledge.generate_dict()}


def set_orders_input(websocket, data):
    if websocket.game.stage == 1:
        if not isinstance(data.get("order_colors"), dict):
            return {"result": "error", "message": "Invalid data"}
        for x in ["red", "green", "blue", "yellow", "purple", "grey"]:
            if x in data["order_colors"]:
                if not isinstance(data["order_colors"][x], bool):
                    return {"result": "error", "message": "Invalid data"}
            else:
                return {"result": "error", "message": "Invalid data"}
        websocket.game.labs[websocket.pl_uuid].set_orders_input(data["order_colors"])
        return {"result": "ok", "message": "Orders input set"}
    return {"result": "error", "message": "You can't set orders"}


def buy_ad(websocket, data):
    if websocket.game.stage == 1:
        if not isinstance(data.get("count"), int):
            return {"result": "error", "message": "Invalid data"}
        if data["ads_options"] > websocket.game.labs[websocket.pl_uuid].get_money():
            return {"result": "error", "message": "To expensive"}
        websocket.game.labs[websocket.pl_uuid].buy_ad(data["ads_options"])
        return {"result": "ok", "message": "Orders input set"}
    return {"result": "error", "message": "You can't set orders"}


def set_lab_name(websocket, data):
    if len(data["new_lab_name"]) > 20:
        return {"result": "error", "message": "Too long"}
    websocket.game.labs[websocket.pl_uuid].set_name(data["new_lab_name"])
    return {"result": "ok", "message": "Lab name set"}


def set_payment_type(websocket, data):
    if websocket.game.stage == 1:
        if data["payment_type"] not in ["post_pay", "pre_pay"]:
            return {"result": "error", "message": "Invalid data"}
        websocket.game.labs[websocket.pl_uuid].set_payment_type(data["payment_type"])
        return {"result": "ok", "message": "Payment type set"}
    return {"result": "error", "message": "You can't set payment type"}
