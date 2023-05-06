import json
import pickle

from pymongo import MongoClient
from yaml import load, Loader

data = load(open('configs/db.yaml'), Loader=Loader)


class UserMongo:
    database = MongoClient(
        "mongodb://" + data["login"] + ":" + data["password"] + "@" + data["host"] + ":" + str(data["port"]))[
        data["database"]]

    @staticmethod
    def get_collection():
        return UserMongo.database[data["users"]["collection"]]

    @staticmethod
    def add_user(login: str, password: str, privilege: bool = False):
        if UserMongo.get_user(login) is None:
            UserMongo.get_collection().insert_one(
                {"login": login, "password": password, "games": {}, "privilege": privilege})
            return True
        else:
            return False

    @staticmethod
    def get_user(login: str):
        return UserMongo.get_collection().find_one({"login": login})

    @staticmethod
    def delete_user(login: str):
        UserMongo.get_collection().delete_one({"login": login})

    @staticmethod
    def add_privilege(login: str):
        user = UserMongo.get_user(login)
        if user is not None:
            if not user["privilege"]:
                UserMongo.get_collection().update_one({"login": login}, {"$set": {"privilege": True}})
                return True, "Privilege added"
            else:
                return False, "User already have privilege"
        else:
            return False, "User not found"

    @staticmethod
    def delete_privilege(login: str):
        user = UserMongo.get_user(login)
        if user is not None:
            if user["privilege"]:
                UserMongo.get_collection().update_one({"login": login}, {"$set": {"privilege": False}})
                return True, "Privilege deleted"
            else:
                return False, "User already don't have privilege"
        else:
            return False, "User not found"

    @staticmethod
    def add_player_to_game(login: str, game_uuid: str, player_uuid: str):
        user = UserMongo.get_user(login)
        if user is not None:
            if game_uuid not in user["games"]:
                UserMongo.get_collection().update_one({"login": login}, {"$set": {"games." + game_uuid: player_uuid}})
                return True, "Player added"
            else:
                return False, "Player already in game"
        else:
            return False, "User not found"

    @staticmethod
    def remove_player_from_game(pl_login, ga_uuid):
        user = UserMongo.get_collection().find_one({"login": pl_login})
        if user is not None:
            UserMongo.get_collection().update_one({"login": user["login"]}, {"$unset": {"games." + ga_uuid: ""}})
            return True, "Player removed"
        else:
            return False, "Player not found"


class GameMongo:
    database = MongoClient(
        "mongodb://" + data["login"] + ":" + data["password"] + "@" + data["host"] + ":" + str(data["port"]))[
        data["database"]]

    @staticmethod
    def get_collection():
        return GameMongo.database[data["games"]["collection"]]

    @staticmethod
    def add_game(game):
        if GameMongo.get_game(game.get_uuid()) is None:
            GameMongo.get_collection().insert_one({
                "game": pickle.dumps(game),
                "game_uuid": game.get_uuid()
            })
            return True
        else:
            return False

    @staticmethod
    def get_game(uuid: str):
        game = GameMongo.get_collection().find_one({"game_uuid": uuid})
        if game is not None:
            return pickle.loads(game["game"])
        else:
            return None

    @staticmethod
    def archive_game(game):
        if GameMongo.get_game(game.get_uuid()):
            GameMongo.get_collection().insert_one({
                "game": json.dumps(game.generate_dict()),
                "month": game.month,
                "stage": game.stage,
                "archive": "true",
                "game_uuid": "archive_" + game.get_uuid()
            })
            return True
        else:
            return False

    @staticmethod
    def get_archive_game_of_period(start, end):
        if start > end:
            start, end = end, start
        start = int(start)
        end = int(end)
        result = []
        for i in range(start, end):
            game = GameMongo().get_collection().find_one({"$and": [{"archive": "true"}, {"month": i}]})
            if game:
                result.append(game)
        return result

    @staticmethod
    def get_archive_game(uuid):
        game = GameMongo.get_collection().find_one({"game_uuid": "archive_" + uuid})
        if game is not None:
            return pickle.loads(game["game"])
        else:
            return None

    @staticmethod
    def delete_game(uuid: str):
        GameMongo.get_collection().delete_one({"game_uuid": uuid})

    @staticmethod
    def update_game(game):
        GameMongo.get_collection().update_one({"game_uuid": game.get_uuid()},
                                              {"$set": {"game": pickle.dumps(game)}})

    @staticmethod
    def get_all_games():
        return GameMongo.get_collection().find()
