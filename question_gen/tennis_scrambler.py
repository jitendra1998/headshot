from collections import defaultdict
import xlrd
import random
import redis as rd
import json
import csv
import os

red = rd.StrictRedis('localhost', db=10)
red1 = rd.StrictRedis('localhost', db=11)


class TennisScrambler(object):
    def __init__(self):
        self.csv_path = 'tennis.xlsx'
        self.quest ={}
        self.ans = defaultdict(list)
        self.correct_ans = defaultdict(list)
        self.hint1 = defaultdict(list)
        self.hint2 = defaultdict(list)
        self.hint3 = defaultdict(list)

        self.type = defaultdict(list)
        self.category = defaultdict(list)

        pass

    def import_csv(self, sheet_index):
        workbook = xlrd.open_workbook(self.csv_path)
        worksheet = workbook.sheet_by_index(sheet_index)

        # Set to 0 if you want to include the header data.
        offset = 0
        total_rows = []
        for i, single_row in enumerate(range(worksheet.nrows)):
        # for i, single_row in enumerate(range(10)):
        #     if i <= offset:  # (Optionally) skip headers
        #         continue
            r = []
            for j, single_row in enumerate(range(worksheet.ncols)):
                if len(str(worksheet.cell_value(i,j))) ==0:
                    r.append(None)
                else:
                    r.append((worksheet.cell_value(i, j)))
            total_rows.append(r)
        return total_rows

    def questions_from_csv(self, sheet_index):
        if sheet_index == 1:
            rows = self.import_csv(sheet_index)
            rows[0] = [ele.lower().strip() for ele in rows[0] if ele]
            print(rows[0])

            question_id = rows[0].index('question')

            a_1_id = rows[0].index('correct answer')
            a_2_id = rows[0].index('correct answer 2')
            a_3_id = rows[0].index('answer 3')
            a_4_id = rows[0].index('answer 4')

            hint_0_a = rows[0].index('category_1')
            hint_1_a = rows[0].index('category 2_a')
            hint_2_a = rows[0].index('category 2_b')
            hint_3_a = rows[0].index('category_3')

            for col in range(len(rows)):
                if rows[col][question_id]:
                    if col==0:
                        continue

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
                        self.correct_ans[col].append(self.ans[col].index(rows[col][a_2_id]))

                        self.hint1[col].append(rows[col][hint_0_a])
                        self.hint1[col].append(rows[col][hint_1_a])
                        self.hint1[col].append(rows[col][hint_2_a])
                        self.hint1[col].append(rows[col][hint_3_a])

                else:
                    continue

        elif sheet_index == 0:
            rows = self.import_csv(sheet_index)
            rows[0] = [ele.lower().strip() for ele in rows[0] if ele]
            print(rows[0])

            question_id = rows[0].index('question')

            a_1_id = rows[0].index('correct answer')
            a_2_id = rows[0].index('answer 1')
            a_3_id = rows[0].index('answer 2')
            a_4_id = rows[0].index('answer 3')

            hint_0_a = rows[0].index('category_1')
            hint_1_a = rows[0].index('category 2_a')
            hint_2_a = rows[0].index('category 2_b')
            hint_3_a = rows[0].index('category_3')

            for col in range(len(rows)):
                if rows[col][question_id]:
                    if col == 0:
                        continue

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
                        # self.correct_ans[col].append(self.ans[col].index(rows[col][a_2_id]))

                        self.hint1[col].append(rows[col][hint_0_a])
                        self.hint1[col].append(rows[col][hint_1_a])
                        self.hint1[col].append(rows[col][hint_2_a])
                        self.hint1[col].append(rows[col][hint_3_a])

                else:
                    continue

    def get_questions(self):
        final_dict = {}
        for ele in self.quest:
            ind = str(ele + 10000)
            final_dict[ind] = {}
            final_dict[ind]['ans'] = self.ans[ele]
            final_dict[ind]['question'] = [self.quest[ele]]
            final_dict[ind]['d1'] = self.hint1[ele]
            final_dict[ind]['c_ans'] = self.correct_ans[ele]

        print(len(final_dict), 'This is the tennis')
        with open('tennis.json', 'w') as outfile:
            json.dump(final_dict, outfile, indent=2)



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

        self.football_questions = []
        self.social_sciences = []
        self.sciences = []


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
                    continue
                elif str(rows[col][multi_ans_3]).lower() =='yes':
                    continue
                elif str(rows[col][visual]).lower() == 'yes':
                    continue
                else:

                    if rows[col][hint_1_a].lower() == 'football':

                        if '(Select 2 answers)' not in rows[col][question_id]:
                            if len(rows[col][question_id]) > 5:
                                f = {}
                                ans = []
                                hint = []
                                c_ans = []

                                ans.append(rows[col][a_1_id])
                                ans.append(rows[col][a_2_id])
                                ans.append(rows[col][a_3_id])
                                ans.append(rows[col][a_4_id])
                                random.shuffle(ans)

                                hint.append(rows[col][hint_0_a])
                                hint.append(rows[col][hint_1_a])
                                hint.append(rows[col][hint_2_a])
                                hint.append(rows[col][hint_3_a])

                                c_ans.append(ans.index(rows[col][a_1_id]))

                                f['ans'] = ans
                                f['c_ans'] = c_ans
                                f['question'] = [rows[col][question_id]]
                                f['d1'] = hint

                                self.football_questions.append(f)


                    elif rows[col][hint_0_a].lower() == 'social sciences':

                        if '(Select 2 answers)' not in rows[col][question_id]:
                            if len(rows[col][question_id]) > 5:
                                f = {}
                                ans = []
                                hint = []
                                c_ans = []

                                ans.append(rows[col][a_1_id])
                                ans.append(rows[col][a_2_id])
                                ans.append(rows[col][a_3_id])
                                ans.append(rows[col][a_4_id])
                                random.shuffle(ans)

                                hint.append(rows[col][hint_0_a])
                                hint.append(rows[col][hint_1_a])
                                hint.append(rows[col][hint_2_a])
                                hint.append(rows[col][hint_3_a])

                                c_ans.append(ans.index(rows[col][a_1_id]))

                                f['ans'] = ans
                                f['c_ans'] = c_ans
                                f['question'] = [rows[col][question_id]]
                                f['d1'] = hint

                                self.social_sciences.append(f)

                    elif rows[col][hint_0_a].lower() == 'sciences':

                        if '(Select 2 answers)' not in rows[col][question_id]:
                            if len(rows[col][question_id]) > 5:
                                f = {}
                                ans = []
                                hint = []
                                c_ans = []

                                ans.append(rows[col][a_1_id])
                                ans.append(rows[col][a_2_id])
                                ans.append(rows[col][a_3_id])
                                ans.append(rows[col][a_4_id])
                                random.shuffle(ans)

                                hint.append(rows[col][hint_0_a])
                                hint.append(rows[col][hint_1_a])
                                hint.append(rows[col][hint_2_a])
                                hint.append(rows[col][hint_3_a])

                                c_ans.append(ans.index(rows[col][a_1_id]))

                                f['ans'] = ans
                                f['c_ans'] = c_ans
                                f['question'] = [rows[col][question_id]]
                                f['d1'] = hint

                                self.sciences.append(f)

        temp = {}
        for num in range(len(self.football_questions)):
            temp[str(num + 20000)] = self.football_questions[num]

        with open('football.json', 'w') as outfile:
            json.dump(temp, outfile, indent=2)

        temp = {}
        for num in range(len(self.social_sciences)):
            temp[str(num + 30000)] = self.social_sciences[num]

        with open('social_sciences.json', 'w') as outfile:
            json.dump(temp, outfile, indent=2)

        temp = {}
        for num in range(len(self.sciences)):
            temp[str(num + 40000)] = self.sciences[num]

        with open('sciences.json', 'w') as outfile:
            json.dump(temp, outfile, indent=2)


if __name__ == '__main__':
    obj = TennisScrambler()
    obj.questions_from_csv(0)
    print(len(obj.quest))
    obj.get_questions()
    obj1 = QuestionFromCsv()
    obj1.questions_from_csv()
    print(len(obj1.football_questions), 'This is football questions')
    print(len(obj1.social_sciences), 'This is a Social Science')
    print(len(obj1.sciences), 'This is a Science')
    print('populated')

