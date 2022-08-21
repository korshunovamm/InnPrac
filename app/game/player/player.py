from uuid import uuid4
from hashlib import sha256, new

from pefile import b


class Player(object):
    _dynamic = {
        
    }
    _money: int = 120
    _nickname: str = ""
    _hash: str = ""
    _uuid: str = uuid4()
    _services: object = {

    }

    def __init__(self, nickname: str, password: str):
        self._nickname = nickname
        self._hash = sha256(password.encode('utf-8')).hexdigest()