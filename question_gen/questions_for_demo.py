import json
import random
import redis as rd
import tornado, tornado.web
from user_statistics import UserStatistics
red1 = rd.StrictRedis('localhost', db=12)

import ast
import os



class GameTableMapping(object):
    def __init__(self):
        self.all_questions =[]
        self.redis_initialization()
        with open('op.json') as json_data:
            self.master = json.load(json_data)

    def random_generator(self):
        return random.randint(0, 11700)
        pass

    def redis_initialization(self):
        if red1.get('unique_num'):
            self.unique_num = json.loads(red1.get('unique_num').decode('utf-8'))
        else:
            self.unique_num = {}

        if red1.get('question_on_table'):
            self.question_on_table = json.loads(red1.get('question_on_table').decode('utf-8'))
        else:
            self.question_on_table = {}

        pass


    def return_latest_id(self, game_id, theme):
        all_users = [str(user) for user in game_id[list(game_id.keys())[0]]]
        table_no = str(list(game_id.keys())[0])
        self.fetch_all_questions(all_users)
        u_id = str(self.unique_id_gen(all_users, theme))
        if table_no in self.question_on_table:
            self.question_on_table[table_no].append(u_id)
        else:
            self.question_on_table[table_no] = [u_id]
        red1.set('question_on_table', json.dumps(self.question_on_table))
        self.update_table_info(table_no, theme, u_id)
        return u_id

    def update_table_info(self, table_no, theme, uid):
        if red1.get('table_info'):
            table_info = json.loads(red1.get('table_info').decode('utf-8'))
        else:
            table_info={}
        temp = []
        temp.append(theme)
        temp.append(str(uid))

        table_info[table_no] = '|'.join(temp)
        red1.set('table_info', json.dumps(table_info))
        pass


    def fetch_all_questions(self, all_users):
        for user in all_users:
            if (user) in self.unique_num:
                self.all_questions.extend(self.unique_num[user])
        pass

    def unique_id_gen(self, all_users, theme):
        num = self.random_generator()
        if num not in self.all_questions:
            for user in all_users:
                if user in self.unique_num:
                    self.unique_num[user].append(num)
                else:
                    self.unique_num[user] = [num]
            red1.set('unique_num', json.dumps(self.unique_num))

            return num
        else:
            self.unique_id_gen(all_users, theme)
        pass


class QuestionGen(tornado.web.RequestHandler):

    def set_headers(self):
        self.set_header('Content-Type', 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')

    def post(self):
        self.set_headers()
        game_id = ast.literal_eval(self.get_argument('Game_Room_id'))
        theme = str(self.get_argument('theme'))
        with open('op.json') as json_data:
            return_dict = json.load(json_data)
        try:

            uid = game_table_mapping_obj.return_latest_id(game_id, theme)
            print(uid)
            self.write(json.dumps({
                                    'success':{
                                                'code':200,
                                                'data':return_dict[uid]
                                                }
                                                }))
        except KeyError as e:
            self.write(json.dumps({
                'error': {
                    'code': 405,
                    'data': 'Insufficient Questions'
                }
            }))
            self.finish()

class QuestionStatistics(tornado.web.RequestHandler):
    def set_headers(self):
        self.set_header('Content-Type', 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')

    def post(self):
        self.set_headers()
        user_data = ast.literal_eval(self.get_argument('user_data'))
        user_stat_obj.run(user_data)
        self.write(json.dumps({
            'success': {
                'code': 200
            }
        }))
        self.finish()
    pass

application = tornado.web.Application([
        (r"/question", QuestionGen),
        (r"/question_statistics", QuestionStatistics),
        ], debug=True)


if __name__ == "__main__":
    application.listen(8088)

    game_table_mapping_obj = GameTableMapping()
    user_stat_obj = UserStatistics()
    print("Server started @ 8088")
tornado.ioloop.IOLoop.instance().start()

