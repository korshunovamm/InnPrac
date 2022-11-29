import pickle

from server.mongoDB import GameMongo

if __name__ == '__main__':
    uuid = "9128d67ce5a84889a330fc20f7a534ac"
    game = pickle.loads(GameMongo.get_collection().find_one({"game_uuid": uuid})["game"])
    pass