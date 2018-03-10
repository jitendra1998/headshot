import json
import redis as rd
# red1 = rd.StrictRedis('localhost', db=11)
red1 = rd.StrictRedis('localhost', db=12) # Used for Demo
import numpy as np


'''
Input :- {game_room_id :{user_id: correct_ans(1) or wrong_ans(0)|time taken to click the ans }}

'''


class UserStatistics(object):

    def __init__(self):
        self.redis_initialization()
        pass

    def redis_initialization(self):
        if red1.get('user_statistics'):
            self.user_statistics = json.loads(red1.get('user_statistics').decode('utf-8'))
        else:
            self.user_statistics = {}

        if red1.get('question_difficulty'):
            self.question_difficulty = json.loads(red1.get('question_difficulty').decode('utf-8'))
        else:
            self.question_difficulty = {}

        if red1.get('user_difficulty'):
            self.user_difficulty = json.loads(red1.get('user_difficulty').decode('utf-8'))
        else:
            self.user_difficulty = {}

    def user_mapping(self, user_dict):
        total_ans, total_time, = 0, 0
        table_info = json.loads(red1.get('table_info').decode('utf-8'))
        for game_room_id in user_dict:
            theme, uid = table_info[game_room_id].split('|')
            for (user) in user_dict[game_room_id]:
                ans, time = user_dict[game_room_id][user].split('|')

                if user in self.user_statistics:
                    if theme in self.user_statistics[user]:
                        if ans == '1':
                            temp = []
                            correct_ans, total = self.user_statistics[user][theme].split('|')
                            temp.append(str(int(correct_ans)+1))
                            temp.append(str(int(total)+1))
                            self.user_statistics[user][theme] = '|'.join(temp)

                            temp = []
                            correct_ans, total = self.user_statistics[user]['total'].split('|')
                            temp.append(str(int(correct_ans) + 1))
                            temp.append(str(int(total) + 1))
                            self.user_statistics[user]['total'] = '|'.join(temp)

                        if ans == '0':
                            temp = []
                            correct_ans, total = self.user_statistics[user][theme].split('|')
                            temp.append(str(int(correct_ans)))
                            temp.append(str(int(total) + 1))

                            self.user_statistics[user][theme] = '|'.join(temp)

                            temp = []
                            correct_ans, total = self.user_statistics[user]['total'].split('|')
                            temp.append(str(int(correct_ans)))
                            temp.append(str(int(total) + 1))
                            self.user_statistics[user]['total'] = '|'.join(temp)
                    else:
                        if ans == '1':
                            temp = []
                            correct_ans, total = 0, 0

                            temp.append(str(int(correct_ans) + 1))
                            temp.append(str(int(total) + 1))
                            self.user_statistics[user][theme] = {}
                            self.user_statistics[user][theme] = '|'.join(temp)

                            temp = []
                            correct_ans, total = 0, 0
                            temp.append(str(int(correct_ans) + 1))
                            temp.append(str(int(total) + 1))
                            self.user_statistics[user]['total'] = '|'.join(temp)

                        if ans == '0':
                            temp = []
                            correct_ans, total = 0, 0
                            temp.append(str(int(correct_ans)))
                            temp.append(str(int(total) + 1))
                            self.user_statistics[user][theme] = {}
                            self.user_statistics[user][theme] = '|'.join(temp)

                            temp = []
                            correct_ans, total = 0, 0
                            temp.append(str(int(correct_ans)))
                            temp.append(str(int(total) + 1))
                            self.user_statistics[user]['total'] = '|'.join(temp)


                else:
                    if ans =='0':
                        self.user_statistics[user] = {}
                        self.user_statistics[user][table_info[game_room_id].split('|')[0]] = '0|1'
                        self.user_statistics[user]['total'] = '0|1'

                    elif ans =='1':
                        self.user_statistics[user] = {}
                        self.user_statistics[user][table_info[game_room_id].split('|')[0]] = '1|1'
                        self.user_statistics[user]['total'] = '1|1'

                total_ans += float(ans)
                total_time = total_time + (float(time)/10.0)
            num_of_user = float(len(user_dict[game_room_id]))
            score = (float((num_of_user-total_ans)/num_of_user)*100 + (total_time/num_of_user)*100)/2
            if uid in self.question_difficulty:

                self.question_difficulty[uid] = str((float(self.question_difficulty[uid])+ score)/2)
            else:
                self.question_difficulty[uid] = str(score)


            for user in user_dict[game_room_id]:
                if user in self.user_difficulty:
                    if theme in self.user_difficulty[user]:
                        self.user_difficulty[user][theme] = str((float(self.user_difficulty[user][theme]) + score)/2)
                    else:
                        self.user_difficulty[user][theme] = str(score)
                else:
                    self.user_difficulty[user] = {}
                    self.user_difficulty[user][theme] = str(score)

        red1.set('user_statistics', json.dumps(self.user_statistics))
        red1.set('question_difficulty', json.dumps(self.question_difficulty))
        red1.set('user_difficulty', json.dumps(self.user_difficulty))
        return True

    def run(self, user_dict):
        return self.user_mapping(user_dict)
        pass

if __name__ == '__main__':
    obj = UserStatistics()
    user_dict = {'2': {'252': '0|9', }, '3': {'2600': '0|1.5', '302': '0|5', '96': '0|5'}}
    obj.run(user_dict)
    print(obj.user_statistics)
    print(obj.question_difficulty)
    print(obj.user_difficulty)
    pass