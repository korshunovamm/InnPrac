from server.api.game.connect_game import ConnectToGame
from server.api.game.delete_user import DeleteUserFromGame
from server.api.game.get_game_from_archive import GetGameFromArchive
from server.api.game.go_to_next_stage import GoToNextStage
from server.api.game.new_game import NewGame
from server.api.users.add_privilege import AddPrivilege
from server.api.users.get_user_info import GetUserInfo
from server.api.users.join_game import JoinGame
from server.api.users.login.auth import Authorization
from server.api.users.login.register import Register
from server.api.game.start_game import StartGame


def setup_routers(app):
    app.add_handlers(".*$", [
        (r"/add_privilege", AddPrivilege),
        (r"/register", Register),
        (r"/login", Authorization),
        (r"/get_user_info", GetUserInfo),
        (r"/join_game/.*", JoinGame),
        (r"/new_game", NewGame),
        (r"/connect_game", ConnectToGame),
        (r"/start_game", StartGame),
        (r"/go_to_next_stage", GoToNextStage),
        (r"/get_game_from_archive", GetGameFromArchive),
        (r"/delete_user_from_game", DeleteUserFromGame),
    ])
