import tornado

from server.api.users.login.auth import get_user_info


class GetUserInfo(tornado.web.RequestHandler):
    def post(self):
        jwt_text = self.get_cookie("user")
        if jwt_text:
            status, user = get_user_info(jwt_text)
            if status:
                self.write({'status': 'ok', 'data': user})
                self.set_status(200)
            else:
                self.write({'status': 'error', 'message': 'Invalid token'})
                self.set_status(401)
        else:
            self.redirect("/login?redirect=" + self.request.path)
            self.set_status(401)