from server.api.game.connect_game import ConnectToGame
from server.api.game.new_game import NewGame
from server.api.users.add_privilege import AddPrivilege
from server.api.users.get_user_info import GetUserInfo
from server.api.users.join_game import JoinGame
from server.api.users.login.auth import Authorization
from server.api.users.login.register import Register
from server.api.users.start_game import StartGame
from server.api.users.unjoin_game import UnjoinGame


def setup_routers(app):
    app.add_handlers(".*$", [
        (r"/add_privilege", AddPrivilege),  # This is a POST request, not a GET request.
        (r"/register", Register),  # This is a POST request, not a GET request.
        (r"/login", Authorization),  # This is a POST request, not a GET request."
        (r"/get_user_info", GetUserInfo),
        (r"/join_game/.*", JoinGame),
        (r"/new_game", NewGame),  # This is a GET request, not a POST request.
        (r"/connect_game", ConnectToGame),  # This is a POST request, not a GET request.
        (r"/unjoin_game", UnjoinGame),  # This is a POST request, not a GET request.
        (r"/start_game", StartGame),  # This is a POST request, not a GET request.
    ])
