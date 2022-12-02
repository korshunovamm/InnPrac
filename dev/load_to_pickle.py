import pickle

from server.mongoDB import GameMongo

if __name__ == '__main__':
    uuid = "4664cb345db84860956c97d4d36d5416"
    game = pickle.loads(GameMongo.get_collection().find_one({"game_uuid": uuid})["game"])
    print(game.generate_dict())
