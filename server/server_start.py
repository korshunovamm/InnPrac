import asyncio

import tornado.web

from server.routes import setup_routers


async def main():
    app = tornado.web.Application()
    setup_routers(app)
    app.listen(8888)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
