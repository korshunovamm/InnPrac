from tornado.web import RequestHandler

from server.api.users.login.auth import get_user_info
from server.mongoDB import GameMongo


class GetUserInfo(RequestHandler):
    def get(self):
        jwt_text = self.get_cookie("user")
        if jwt_text:
            status, user = get_user_info(jwt_text)
            if status:
                for x in user['games']:
                    ga = GameMongo.get_game(x)
                    user['games'][x] = dict(uuid=x, name=ga.get_name(), status=ga.get_status(),
                                            pl_uuid=user['games'][x])
                del user['password']
                del user['_id']
                self.write({'status': 'ok', 'data': user})
                self.set_status(200)
            else:
                self.write({'status': 'error', 'message': 'Invalid token'})
                self.set_status(401)
        else:
            self.redirect("/login?redirect=" + self.request.path)
            self.set_status(401)
