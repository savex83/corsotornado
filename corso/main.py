import time
import json

import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado import gen


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class MainJsonEchoHandler(tornado.web.RequestHandler):
    def get(self):
        nome = self.get_argument("param", default='')
        nome2 = self.get_argument("param2", default='')
        result = int(nome) + int(nome2)
        self.write(json.dumps({'param': nome, 'param2': nome2, 'result': result}))


class MainHomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/home.html")


# /echo/web/
class MainWebEchoHandler(tornado.web.RequestHandler):
    def get(self):
        param = self.get_argument("param", default=0)
        param1 = self.get_argument("altro", default=0)
        result = int(param) + int(param1)
        dizionario = {'param': param,
                      'param1': param1,
                      'result': result}
        # self.render("templates/echo.html", result=result, param=param, param1=param1)
        self.render("templates/echo.html", **dizionario)


# WebSocket
class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket aperta")

    def on_message(self, message):
        self.write_message(u"Echo: " + message)

    def on_close(self):
        print("WebSocket chiusa")


class MainWsHomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/home_ws.html")


# /websocket/clock/
class ClockWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket aperta")

    async def on_message(self, message):
        await gen.sleep(1)
        self.write_message(u"Orario: %s" % time.strftime('%X'))


    def on_close(self):
        print("WebSocket chiusa")


# /home/ws/clock/
class ClockWsHomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/home_ws_clock.html")


# /websocket/counters/
class CountersWebSocket(tornado.websocket.WebSocketHandler):
    ascoltatori = set()
    componenti_prodotti = 0
    componenti_fallati = 0

    def open(self):
        print("WebSocket aperta")
        CountersWebSocket.ascoltatori.add(self)

    def on_message(self, message):
        self.manage_message(message)

    def on_close(self):
        print("WebSocket chiusa")
        CountersWebSocket.ascoltatori.remove(self)

    @classmethod
    def manage_message(cls, message):
        if message == 'ping':
            cls.broadcast_stato()
        elif message == 'ok':
            cls.componenti_prodotti += 1
            cls.broadcast_stato()
        elif message == 'fallato':
            cls.componenti_prodotti += 1
            cls.componenti_fallati += 1
            cls.broadcast_stato()
        else:
            pass

    @classmethod
    def broadcast_stato(cls):
        for ascoltatore in cls.ascoltatori:
            ascoltatore.write_message("Componenti prodotti {} - fallati {}".format(cls.componenti_prodotti,
                                                                                   cls.componenti_fallati))

# /home/ws/counters/
class CountersWsHomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/home_ws_counters.html")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/echo/", MainJsonEchoHandler),
        (r"/echo/web/", MainWebEchoHandler),
        (r"/home/", MainHomeHandler),
        # WS
        (r"/websocket/echo/", EchoWebSocket),
        (r"/home/ws/", MainWsHomeHandler),
        # WS Clock
        (r"/websocket/clock/", ClockWebSocket),
        (r"/home/ws/clock/", ClockWsHomeHandler),
        # Ws Counters
        (r"/websocket/counters/", CountersWebSocket),
        (r"/home/ws/counters/", CountersWsHomeHandler),
    ], autoreload=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()