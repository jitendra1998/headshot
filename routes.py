import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import MySQLdb

from user_api import *
from game_room_api import *
from admin_func import *
from datetime import datetime
from queries import SQLqueries
from messages import errors
from messages import success
from helperfunctions import *

from mysql_configure import MYSQLConfiguration
obj_help = HelpingFunctions()
error_obj = errors()
success_obj = success()
query_obj = SQLqueries()
db_obj = MYSQLConfiguration()

import redis
r = redis.StrictRedis(host='localhost', db=4)

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            cookie_secret="43osdETzKXasdQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            template_path=__file__,
            static_path=__file__
        )

        handlers = [

            # User APIs
            (r"/", WebSite),
            (r"/user/login", UserLogin),
            (r"/authenticate/user", PrivateAccessAutheticate),
            (r"/authenticate/admin", PrivateAccessAutheticateAdmin),
            (r"/admin", AdminLogin),
            (r"/user/signup", UserSignup),
            (r"/user/view_games", Game_room_showall),
            (r"/Websocket/([^/]+)", WebSocketHandler1),
            (r"/user/view_games/Game_Room/([^/]+)/([^/]+)", Game_Room),
            (r"/admin_portal", admin_portal),
            (r"/user/logout", UserLogout),
        ]

        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = MySQLdb.connect(
            db_obj.host, db_obj.user, db_obj.password, db_obj.db, charset='utf8', use_unicode=True)


if __name__ == "__main__":
    __file__ = str(os.getcwd()) + "/quizzycash_html_files/"
    server = Application()
    port = 8080
    server.listen(port)
    #print "Server running:", port
    debug = True
    # server = tornado.httpserver.HTTPServer(ws_app)
    # server.bind(8090)
    # print "Server running on port 8090"
    # server.start(0)
    obj_help.redis_init_tables()
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()


# r.set('active_games', json.dumps({'game1':'1'}))
# r.get('active_players')
# r.get('user_session')
# r.get('active_games')
