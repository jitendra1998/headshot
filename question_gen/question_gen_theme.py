import tornado
from quest_gen import QuestionFromCsv
import tornado.web
import json
from quest_gen import GameTableMapping
import ast
import redis as rd
from similarity import Sentence
red = rd.StrictRedis('localhost', db=10)
red1 = rd.StrictRedis('localhost', db=11)
from collections import defaultdict


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
        return_dict = defaultdict(list)
        try:

            uid = game_table_mapping_obj.return_latest_id(game_id, theme)
            return_dict['question'].append(quet[uid])
            return_dict['ans'].extend(ans[uid])
            return_dict['d1'].extend(hint1[uid])
            return_dict['d2'].extend(hint2[uid])
            return_dict['d3'].extend(hint3[uid])
            return_dict['c_ans'].extend(correct_ans[uid])
            self.write(json.dumps({
                                    'success':{
                                                'code':200,
                                                'data':return_dict
                                                }
                                                }))
        except KeyError as e:
            self.write(json.dumps({
                'error': {
                    'code': 405,
                    'data': 'Insufficient Questions'
                }
            }))
        pass

application = tornado.web.Application([
        (r"/question", QuestionGen),
        ], debug=True)


if __name__ == "__main__":
    application.listen(8088)

    import_quest_obj = QuestionFromCsv()
    import_quest_obj.run()

    quest_similarity_obj = Sentence()
    quest_similarity_obj.run()

    game_table_mapping_obj = GameTableMapping()

    quet = json.loads(red.get('questions').decode('utf-8'))
    ans = json.loads(red.get('ans').decode('utf-8'))
    correct_ans = json.loads(red.get('correct_ans').decode('utf-8'))
    hint1 = json.loads(red.get('hint1').decode('utf-8'))
    hint2 = json.loads(red.get('hint2').decode('utf-8'))
    hint3 = json.loads(red.get('hint3').decode('utf-8'))

    print("Server started @ 8088")
tornado.ioloop.IOLoop.instance().start()
