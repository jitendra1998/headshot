import tornado.web
import itertools
from queries import SQLqueries
query_obj = SQLqueries()
import redis
import json
import MySQLdb
from mysql_configure import MYSQLConfiguration

r = redis.StrictRedis(host='localhost',db=4)
db_obj = MYSQLConfiguration()

class WriteData():
    
    db = MySQLdb.connect(
            # "localhost", "root", "root", "quizycash", charset='utf8', use_unicode=True)
            db_obj.host, db_obj.user, db_obj.password, db_obj.db, charset='utf8', use_unicode=True)

    def get_user_data(self, id):
        game_cursor = self.db.cursor()
        game_show_sql = query_obj.show_user_data % int(id)
        game_cursor.execute(game_show_sql)
        game_desc = game_cursor.description
        column_names = [col[0] for col in game_desc]
        data = [dict(itertools.izip(column_names, row))
                for row in game_cursor.fetchall()]
                
        if data:
            return data
        else:
            return None
        
    def append_player_balance(self,id,balance):
        game_cursor = self.db.cursor()
        #game_show_sql = query_obj.show_active_games % int(id)
        sql_query = "UPDATE `quizycash`.`user` SET `virtual_money`=%f WHERE `id`=%d " %(balance,id)
        game_cursor.execute(sql_query)
        self.db.commit()

class CommonBaseHandler(tornado.web.RequestHandler):
        
    @property
    def db(self):
        return self.application.db

    def set_headers(self):
        self.set_header('Content-Type', 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')

    def get_game_data(self,id):
        game_cursor = self.db.cursor()
        game_show_sql = query_obj.show_active_games % int(id)
        game_cursor.execute(game_show_sql)
        game_desc = game_cursor.description
        column_names = [col[0] for col in game_desc]
        data = [dict(itertools.izip(column_names, row))
                for row in game_cursor.fetchall()]
        if data:
            return data
        else:
            return None
        
    def get_user_data(self, id):
        game_cursor = self.db.cursor()
        game_show_sql = query_obj.show_user_data % int(id)
        game_cursor.execute(game_show_sql)
        game_desc = game_cursor.description
        column_names = [col[0] for col in game_desc]
        data = [dict(itertools.izip(column_names, row))
                for row in game_cursor.fetchall()]
        if data:
            return data
        else:
            return None
    
    def append_player_balance(self,id,balance):
        game_cursor = self.db.cursor()
        #game_show_sql = query_obj.show_active_games % int(id)
        sql_query = "UPDATE `quizycash`.`user` SET `virtual_money`=%f WHERE `id`=%d " %(balance,id)
        game_cursor.execute(sql_query)
        self.db.commit()

    def redis_session_check(self, user_name):
        return json.loads(r.get("user_session").decode('utf-8'))