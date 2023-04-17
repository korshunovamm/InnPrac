from tornado.web import RequestHandler
from yaml import load, Loader

from domain.mongoDB import UserMongo

settings = load(open('../configs/api.yaml'), Loader=Loader)


class AddPrivilege(RequestHandler):
    def post(self):
        if self.request.headers.get('Authorization') == "Bearer " + settings["api_key"]:
            if "login" in self.request.body_arguments:
                login = self.request.body_arguments["login"][0].decode('utf-8')
                res = UserMongo.add_privilege(login)
                if res[0]:
                    self.write({"status": "ok", "message": res[1]})
                    self.set_status(200)
                else:
                    self.write({"status": "error", "message": res[1]})
                    self.set_status(200)
            else:
                self.write({"status": "error", "message": "Bad request"})
                self.set_status(400)
        else:
            self.write({"status": "error", "message": "access denied"})
            self.set_status(403)


