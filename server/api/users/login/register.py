import re
from datetime import datetime
from hashlib import sha256

import jwt
import tornado.web
from yaml import Loader, load

from server.mongoDB import UserMongo
from server.set_default_headers import set_default_headers


class Register(tornado.web.RequestHandler):
    async def post(self):
        if not self.get_cookie("user"):
            if "login" in self.request.body_arguments and "password" in self.request.body_arguments:
                if re.compile("[a-zA-Z0-9]+$").match(
                        self.request.body_arguments["login"][0].decode('utf-8')) and re.compile("[a-zA-Z0-9]+$").match(
                    self.request.body_arguments["password"][0].decode('utf-8')):
                    data = self.request.body_arguments
                    config = load(open('configs/api.yaml'), Loader=Loader)
                    if UserMongo.get_user(data['login'][0].decode('utf-8')):
                        self.write({'status': 'error', 'message': 'User already exists'})
                        self.set_status(200)
                    else:
                        UserMongo.add_user(data['login'][0].decode("utf-8"), sha256(data['password'][0]).hexdigest())
                        jwt_text = jwt.encode({"login": self.request.body_arguments['login'][0].decode('utf-8'),
                                               "exp": str(int(round(datetime.now().timestamp())) + 2629743)},
                                              config["jwt_secret"], algorithm="HS256")
                        self.set_cookie("user", jwt_text)
                        self.write({'status': 'ok', 'message': 'User created'})
                        self.set_status(200)
                else:
                    self.write({'status': 'error', 'message': 'Invalid login or password'})
                    self.set_status(200)
            else:
                self.write({'status': 'error', 'message': 'Bad request'})
                self.set_status(400)
        else:
            self.write({'status': 'error', 'message': 'User already authorized'})
            self.set_status(200)