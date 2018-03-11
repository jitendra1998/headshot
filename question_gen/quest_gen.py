from collections import defaultdict
import xlrd
import random
import redis as rd
import json
import csv
import os

red = rd.StrictRedis('localhost', db=10)
red1 = rd.StrictRedis('localhost', db=11)

'''
This class is used for Importing data from csv to the redis,
'''
class QuestionFromCsv(object):

    def __init__(self):
        # red.flushdb()
        # self.csv_path = os.getcwd()+'/QuizzyCash.xlsx'
        self.csv_path = 'QuizzyCash.xlsx'
        self.quest ={}
        self.ans = defaultdict(list)
        self.correct_ans = defaultdict(list)
        self.hint1 = defaultdict(list)
        self.hint2 = defaultdict(list)
        self.hint3 = defaultdict(list)

        self.type = defaultdict(list)
        self.category = defaultdict(list)

    def import_csv(self):
        workbook = xlrd.open_workbook(self.csv_path)
        worksheet = workbook.sheet_by_index(1)

        # Set to 0 if you want to include the header data.
        offset = 1
        rows = []
        for i, row in enumerate(range(worksheet.nrows)):
        # for i, row in enumerate(range(10)):
            if i <= offset:  # (Optionally) skip headers
                continue
            r = []
            for j, col in enumerate(range(worksheet.ncols)):
                if len(str(worksheet.cell_value(i,j))) ==0:
                    r.append(None)
                else:
                    r.append((worksheet.cell_value(i, j)))

            rows.append(r)
        return rows


    def questions_from_csv(self):
        rows = self.import_csv()
        question_id = rows[0].index('Question')

        a_1_id = rows[0].index('Correct Answer 1')
        a_2_id = rows[0].index('Answer 2')
        a_3_id = rows[0].index('Answer 3')
        a_4_id = rows[0].index('Answer 4')

        multi_ans_2 = rows[0].index('MAQ_2')
        multi_ans_3 = rows[0].index('MAQ_3')

        hint_0_a = rows[0].index('Category 0_A')
        hint_1_a = rows[0].index('Category 1_A')
        hint_2_a = rows[0].index('Category 2_A')
        hint_3_a = rows[0].index('Category 3_A')

        hint_0_b = rows[0].index('Category 0_B')
        hint_1_b = rows[0].index('Category 1_B')
        hint_2_b = rows[0].index('Category 2_B')
        hint_3_b = rows[0].index('Category 3_B')

        hint_0_c = rows[0].index('Category 0_C')
        hint_1_c = rows[0].index('Category 1_C')
        hint_2_c = rows[0].index('Category 2_C')
        hint_3_c = rows[0].index('Category 3_C')

        visual = rows[0].index('Visual')

        for col in range(len(rows)):
            if rows[col][question_id]:
                if col==0:
                    continue


                elif str(rows[col][multi_ans_2]).lower() == 'yes':
                    if rows[col][hint_0_a] in self.category:
                        self.category[rows[col][hint_0_a]].append(col)
                    else:
                        self.category[rows[col][hint_0_a]] = []
                        self.category[rows[col][hint_0_a]].append(col)

                    self.quest[col] = rows[col][question_id]

                    self.ans[col].append(rows[col][a_1_id])
                    self.ans[col].append(rows[col][a_2_id])
                    self.ans[col].append(rows[col][a_3_id])
                    self.ans[col].append(rows[col][a_4_id])
                    random.shuffle(self.ans[col])

                    self.correct_ans[col].append(self.ans[col].index(rows[col][a_1_id]))
                    self.correct_ans[col].append(self.ans[col].index(rows[col][a_2_id]))

                    self.hint1[col].append(rows[col][hint_0_a])
                    self.hint1[col].append(rows[col][hint_1_a])
                    self.hint1[col].append(rows[col][hint_2_a])
                    self.hint1[col].append(rows[col][hint_3_a])

                    self.hint2[col].append(rows[col][hint_0_b])
                    self.hint2[col].append(rows[col][hint_1_b])
                    self.hint2[col].append(rows[col][hint_2_b])
                    self.hint2[col].append(rows[col][hint_3_b])

                    self.hint3[col].append(rows[col][hint_0_c])
                    self.hint3[col].append(rows[col][hint_1_c])
                    self.hint3[col].append(rows[col][hint_2_c])
                    self.hint3[col].append(rows[col][hint_3_c])

                    pass
                elif str(rows[col][multi_ans_3]).lower() =='yes':
                    if rows[col][hint_0_a] in self.category:
                        self.category[rows[col][hint_0_a]].append(col)
                    else:
                        self.category[rows[col][hint_0_a]] = []
                        self.category[rows[col][hint_0_a]].append(col)


                    self.quest[col] = rows[col][question_id]

                    self.ans[col].append(rows[col][a_1_id])
                    self.ans[col].append(rows[col][a_2_id])
                    self.ans[col].append(rows[col][a_3_id])
                    self.ans[col].append(rows[col][a_4_id])
                    random.shuffle(self.ans[col])

                    self.correct_ans[col].append(self.ans[col].index(rows[col][a_1_id]))
                    self.correct_ans[col].append(self.ans[col].index(rows[col][a_2_id]))
                    self.correct_ans[col].append(self.ans[col].index(rows[col][a_3_id]))

                    self.hint1[col].append(rows[col][hint_0_a])
                    self.hint1[col].append(rows[col][hint_1_a])
                    self.hint1[col].append(rows[col][hint_2_a])
                    self.hint1[col].append(rows[col][hint_3_a])

                    self.hint2[col].append(rows[col][hint_0_b])
                    self.hint2[col].append(rows[col][hint_1_b])
                    self.hint2[col].append(rows[col][hint_2_b])
                    self.hint2[col].append(rows[col][hint_3_b])

                    self.hint3[col].append(rows[col][hint_0_c])
                    self.hint3[col].append(rows[col][hint_1_c])
                    self.hint3[col].append(rows[col][hint_2_c])
                    self.hint3[col].append(rows[col][hint_3_c])
                    pass

                else:
                    if rows[col][hint_0_a] in self.category:
                        self.category[rows[col][hint_0_a]].append(col)
                    else:
                        self.category[rows[col][hint_0_a]] = []
                        self.category[rows[col][hint_0_a]].append(col)

                    self.quest[col] = rows[col][question_id]

                    self.ans[col].append(rows[col][a_1_id])
                    self.ans[col].append(rows[col][a_2_id])
                    self.ans[col].append(rows[col][a_3_id])
                    self.ans[col].append(rows[col][a_4_id])
                    random.shuffle(self.ans[col])

                    self.correct_ans[col].append(self.ans[col].index(rows[col][a_1_id]))

                    self.hint1[col].append(rows[col][hint_0_a])
                    self.hint1[col].append(rows[col][hint_1_a])
                    self.hint1[col].append(rows[col][hint_2_a])
                    self.hint1[col].append(rows[col][hint_3_a])

                    self.hint2[col].append(rows[col][hint_0_b])
                    self.hint2[col].append(rows[col][hint_1_b])
                    self.hint2[col].append(rows[col][hint_2_b])
                    self.hint2[col].append(rows[col][hint_3_b])

                    self.hint3[col].append(rows[col][hint_0_c])
                    self.hint3[col].append(rows[col][hint_1_c])
                    self.hint3[col].append(rows[col][hint_2_c])
                    self.hint3[col].append(rows[col][hint_3_c])
            else:
                continue

    def redis_store(self):
        red.set('ans', json.dumps(self.ans))
        red.set('questions', json.dumps(self.quest))
        red.set('correct_ans', json.dumps(self.correct_ans))
        red.set('hint1', json.dumps(self.hint1))
        red.set('hint2', json.dumps(self.hint2))
        red.set('hint3', json.dumps(self.hint3))
        red.set('cat', json.dumps(self.category))
        pass

    def run(self):
        print('Importing Csv')
        self.questions_from_csv()
        print('Storing to redis')
        self.redis_store()
        return True
        pass


'''
This class is to fet unique question id after verifying each user previous questions,
'''

class GameTableMapping(object):
    def __init__(self):
        self.all_questions =[]
        self.redis_initialization()
        self.master = json.loads(red.get('master').decode('utf-8'))

    def random_generator(self, theme='Sports'):
        if theme in self.master:
            r = str(random.randrange(0, 5))
            qids = self.master[theme][r]
            return random.choice(qids)
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
        print(theme)
        all_users = [str(user) for user in game_id[list(game_id.keys())[0]]]
        table_no = str(list(game_id.keys())[0])
        self.fetch_all_questions(all_users)
        u_id = str(self.unique_id_gen(all_users, theme))
        if table_no in self.question_on_table:
            self.question_on_table[table_no].append(u_id)
        else:
            self.question_on_table[table_no] = [u_id]
        red1.set('question_on_table', json.dumps(self.question_on_table))
        return u_id

    def fetch_all_questions(self, all_users):
        for user in all_users:
            if (user) in self.unique_num:
                self.all_questions.extend(self.unique_num[user])
        pass

    def unique_id_gen(self, all_users, theme):
        num = self.random_generator(theme)
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

if __name__ == '__main__':
    # obj = QuestionFromCsv()
    # obj.questions_from_csv()
    # obj.questions_from_csv()
    # obj.redis_store()
    # ans = json.loads(red.get('ans').decode('utf-8'))
    pass