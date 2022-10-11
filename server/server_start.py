import asyncio
import tornado.web
from yaml import Loader, load

from server.routes import setup_routers


async def main():
    data = load(open('configs/api.yaml'), Loader=Loader)
    app = tornado.web.Application(cookie_secret=data["cookie_secret"])
    setup_routers(app)
    app.listen(8888)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
