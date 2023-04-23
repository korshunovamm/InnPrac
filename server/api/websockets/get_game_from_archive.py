import json
import os

from tornado.web import RequestHandler


class GetGameFromArchive(RequestHandler):
    def get(self):
        global start_i
        start = self.get_argument("start", "1_1")
        end = self.get_argument("end", "*")
        ga_uuid = self.get_argument("ga_uuid", None)
        if not os.path.exists("archive/"):
            os.makedirs("archive/")
        if ga_uuid and ga_uuid in os.listdir("archive/"):
            files = os.listdir("archive/" + ga_uuid)
            files.sort()
            result = {}
            try:
                start_i = files.index(start + ".json")
                if end == "*":
                    end_i = len(files)
                else:
                    end_i = files.index(str(end) + ".json") + 1
            except ValueError:
                self.write({"result": "error", "message": "Bad request"})
                self.set_status(400)
                return
            if start_i > end_i:
                start_i, end_i = end_i, start_i
            for i in range(start_i, end_i):
                f = open("archive/" + ga_uuid + "/" + files[i], "r")
                result[files[i].split(".")[0]] = json.loads(f.read())
                f.close()
            self.write({"result": "ok", "message": "Game archive", "data": result})
            self.set_status(200)
        else:
            self.write(dict(result="error", message="Bad request"))
            self.set_status(400)
