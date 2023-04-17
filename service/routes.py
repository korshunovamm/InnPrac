from controllers.server.api.websockets.connect_game import ConnectToGame
from controllers.server.api.websockets.delete_user import DeleteUserFromGame
from controllers.server.api.websockets.get_game_from_archive import GetGameFromArchive
from controllers.server.api.websockets.go_to_next_stage import GoToNextStage
from controllers.server.api.websockets.new_game import NewGame
from domain.server.api.users.add_privilege import AddPrivilege
from domain.server.api.users.get_user_info import GetUserInfo
from domain.server.api.users.join_game import JoinGame
from domain.server.api.users.login.auth import Authorization
from domain.server.api.users.login.register import Register
from controllers.server.api.websockets.start_game import StartGame


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
