from datetime import datetime
from hashlib import sha256
from json import load

import jwt
import tornado
from yaml import Loader, load

from server.mongoDB import UserMongo


class Authorization(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        if not self.get_cookie("user"):
            if "login" in self.request.body_arguments and "password" in self.request.body_arguments:
                data = self.request.body_arguments
                config = load(open('configs/api.yaml'), Loader=Loader)
                user_mongo = UserMongo.get_user(data['login'][0].decode('utf-8'))
                if not user_mongo:
                    self.write({'status': 'error', 'message': 'User does not exist'})
                    self.set_status(200)
                else:
                    if user_mongo['password'] == sha256(data['password'][0]).hexdigest():
                        jwt_text = jwt.encode({"login": data['login'][0].decode('utf-8'),
                                               "exp": str(int(round(datetime.now().timestamp())) + 2629743)},
                                              config["jwt_secret"], algorithm="HS256")
                        self.set_cookie("user", jwt_text, httponly=True)
                        self.write({'status': 'ok', 'message': 'User authorized'})
                        self.set_status(200)
                    else:
                        self.write({'status': 'error', 'message': 'Invalid password'})
                        self.set_status(200)
            else:
                self.write({'status': 'error', 'message': 'Bad request'})
                self.set_status(400)
        else:
            self.write({'status': 'error', 'message': 'User already authorized'})
            self.set_status(200)

    def get(self):
        if self.get_cookie("user"):
            self.redirect("/")
        else:
            self.write("Когда нибудь тут будет страница логина")


def get_user_info(jwt_text):
    try:
        login = jwt.decode(jwt_text, load(open('configs/api.yaml'), Loader=Loader)["jwt_secret"], algorithms=["HS256"])[
            "login"]
        user = UserMongo.get_user(login)
        if user:
            return True, user
        return False, None
    except Exception as e:
        return False, None
