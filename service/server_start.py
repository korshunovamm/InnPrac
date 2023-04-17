import asyncio
import os

import tornado.web
import yaml


from service.routes import setup_routers

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader, Dumper


async def main():
    port = yaml.load(open("../configs/api.yaml", "r"), Loader=Loader)['port']
    app = tornado.web.Application()
    setup_routers(app)
    app.listen(port)
    await asyncio.Event().wait()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    asyncio.run(main())
