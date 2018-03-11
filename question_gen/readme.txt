####################### Question Generation From Csv ##############################

Redis DataBase (db=10, db=11) are reserved for the data population and user history.

It runs on python 2 & 3,
packages require:-
'xlrd'
'tornado'
'redis'


question_gen_theme.py ---> It runs on localhost:8088 ---> populate DataBase.

        localhost:8088/question ---->
                input :- 'Game_Room_id' # {'2':['25']}
			  'theme' # 'Sports'
                output :- Questions and options.


questions_for_demo.py ---> It runs on localhost:8088
s
        localhost:8088/question ---->
                input :- 'Game_Room_id' # {'2':['25']}
			  'theme' # 'Sports'
                output :- Questions and options.


In case of any failure in data population please check the path saved in 'question_gen.py'

##########################################################################################
