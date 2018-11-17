import tornado.ioloop
import tornado.web

import json


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class MainJsonEchoHandler(tornado.web.RequestHandler):
    def get(self):
        nome = self.get_argument("nome", default='')
        self.write(json.dumps({'nome': nome}))


class MainHomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/home.html")


class MainWebEchoHandler(tornado.web.RequestHandler):
    def get(self):
        nome = self.get_argument("nome", default='')
        self.render("templates/echo.html", nome=nome)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/echo/", MainJsonEchoHandler),
        (r"/echo/web/", MainWebEchoHandler),
        (r"/home/", MainHomeHandler),
    ], autoreload=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()