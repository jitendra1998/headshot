import random
# import numpy as np
import redis as rd
import json
import math
from common import CommonBaseHandler

r = rd.StrictRedis('localhost',db=4)
red = rd.StrictRedis('localhost',db=4)

'''Input to this function is a list of active players in a gameroom. So active_player_list = ['active_player_id1','active_player_id1'..]'''


class HelpingFunctions(object):
    def select_player(self, active_player_list,game_room_id):
        player_sequence = []
        player = random.choice(active_player_list)
        player_sequence.append(player)
        index = active_player_list.index(player)
        active_player_list.pop(index)
        while len(active_player_list)!=0:
            if index<=len(active_player_list)-1:
                player = active_player_list.pop(index)
                player_sequence.append(player)
            elif index>=len(active_player_list) and len(active_player_list)!=0:
                player_sequence.extend([active_player_list.pop(0) for i in xrange(len(active_player_list))])
            else:
                break
        if r.get('shuffled_active_players'):
            shuffled_active_players = json.loads(r.get('shuffled_active_players').decode('utf-8'))
        else:
            shuffled_active_players = {}
        shuffled_active_players[game_room_id] = player_sequence
        self.redis_store('shuffled_active_players', shuffled_active_players)

    def start_game(self, game_room_id):
        # play small and big blind
        kk = json.loads(red.get('active_set').decode('utf-8'))
        active_set = kk[game_room_id]
        # active_player_list = self.redis_fetch('shuffled_active_players')[game_room_id]
        active_player_list = [ele for ele in self.redis_fetch('shuffled_active_players')[game_room_id] if
                              ele in active_set['total_amount'].keys()]
        active_set['total_amount'][active_player_list[2%len(active_player_list)]] = float(active_set['total_amount'][active_player_list[2%len(active_player_list)]]) - float(active_set['big_blind'])
        active_set['total_amount'][active_player_list[1%len(active_player_list)]] = float(active_set['total_amount'][active_player_list[1%len(active_player_list)]]) - float(active_set['small_blind'])
        active_set['player_bet'][active_player_list[2%len(active_player_list)]] = active_set['big_blind']
        active_set['player_bet'][active_player_list[1%len(active_player_list)]] = active_set['small_blind']
        active_set['pot_amount'] = active_set['pot_amount'] + active_set['big_blind'] + active_set['small_blind']
        active_set['current_max_bet'] = active_set['big_blind']

        kk[game_room_id] = active_set
        self.redis_store('active_set', kk)

        # initializing right ans to an empty list, when the game is initialised
        right_ans = json.loads(r.get('right_ans'))
        right_ans[game_room_id] = {}
        red.set('right_ans', json.dumps(right_ans))

        # change last player of betting round
        red.set('higgest_bidder', active_player_list[2%len(active_player_list)])

    def divide_cash_len(self, game_room_id,usr):
        kk = json.loads(red.get('active_set').decode('utf-8'))
        active_set = kk[game_room_id]

        active_set['total_amount'][usr] = float(active_set['total_amount'][usr]) + float(active_set['pot_amount'])

        # reset pot
        active_set['pot_amount'] = 0
        active_players = active_set['player_bet'].keys()
        active_set['player_bet'] = {usr_id:0 for usr_id in active_players}

        kk[game_room_id] = active_set
        red.set('active_set', json.dumps(kk))

    def divide_cash(self, game_room_id):
        #right_ans {game_room_id: [list of correct player_id's]}
        right_ans_usrs = self.redis_fetch('right_ans')[str(game_room_id)]
        kk = json.loads(red.get('active_set').decode('utf-8'))
        active_set = kk[game_room_id]

        #not optmized correctly
        if bool(right_ans_usrs):
            for usr in active_set['player_bet'].keys():
                if usr in right_ans_usrs.keys():
                    active_set['total_amount'][usr] = float(active_set['total_amount'][usr]) + math.floor((float(active_set['pot_amount'])/len(right_ans_usrs.keys()))*0.9)
                else:
                    continue
            # reset pot
            active_set['pot_amount'] = 0

        active_players = active_set['player_bet'].keys()
        active_set['player_bet'] = {usr_id:0 for usr_id in active_players}

        kk[game_room_id] = active_set
        red.set('active_set', json.dumps(kk))

    def redis_fetch(self, table_name):
        return json.loads(red.get(str(table_name)).decode('utf-8'))

    def redis_store(self, table_name, table_content):
        return red.set(table_name, json.dumps(table_content))

    # def bet(usr_input,game_room_id):
    def bet(self, usr_id,game_room_id, bet_amount):
        kk = self.redis_fetch('active_set')
        active_set = kk[game_room_id]

        # fetching
        total_amount = float(active_set['total_amount'][usr_id])
        current_max_bet = float(active_set['current_max_bet'])
        player_bet = float(active_set['player_bet'][usr_id])

        # calculating
        active_set['total_amount'][usr_id] = total_amount - bet_amount
        active_set['current_max_bet'] = player_bet + bet_amount
        active_set['player_bet'][usr_id] = player_bet + bet_amount

        # updating pot
        active_set['pot_amount'] = active_set['pot_amount'] + bet_amount

        kk[game_room_id] = active_set
        self.redis_store('active_set',kk)

        # change last player of betting round
        red.set('higgest_bidder', usr_id)

    def call(self, usr_id,game_room_id):
        kk = self.redis_fetch('active_set')
        active_set = kk[game_room_id]

        # fetching
        total_amount = float(active_set['total_amount'][usr_id])
        current_max_bet = float(active_set['current_max_bet'])
        player_bet = float(active_set['player_bet'][usr_id])
        call_amount = current_max_bet - player_bet

        # calculating
        active_set['total_amount'][usr_id] = total_amount - call_amount
        active_set['player_bet'][usr_id] = player_bet + call_amount

        # updating pot
        active_set['pot_amount'] = active_set['pot_amount'] + call_amount

        kk[game_room_id] = active_set
        self.redis_store('active_set',kk)

    def fold(self, usr_id,game_room_id):
        kk = self.redis_fetch('shuffled_active_players')
        print kk, 'This is shuffled Active Players'
        active_player_list = kk[game_room_id]
        print 'This is fold'
        if usr_id in active_player_list:
            active_player_list.pop(active_player_list.index(usr_id))
        else:
            pass
        kk[game_room_id] = active_player_list
        self.redis_store('shuffled_active_players',kk)

    def all_in(self, usr_id,game_room_id):
        kk = self.redis_fetch('active_set')
        active_set = kk[game_room_id]
        # fetching
        allin_amount = float(active_set['total_amount'][usr_id])
        current_max_bet = float(active_set['current_max_bet'])
        player_bet = float(active_set['player_bet'][usr_id])
        print allin_amount, 'This is all in amount'
        # calculating
        active_set['total_amount'][usr_id] = 0
        active_set['player_bet'][usr_id] = player_bet + allin_amount
        if active_set['player_bet'][usr_id] > current_max_bet:
            active_set['current_max_bet'] = active_set['player_bet'][usr_id]
            # change last player of betting round
            red.set('higgest_bidder', usr_id)

        # updating pot
        active_set['pot_amount'] = active_set['pot_amount'] + allin_amount

        kk[game_room_id] = active_set
        print  active_set, 'This is active set'
        self.redis_store('active_set',kk)

    def redis_init_tables(self):
        NULL = -1
        print
        sql_data = [
            (0, 'game1', 'soccer-world-cup', 10, 'sports', 1, 10, 1, '2017-08-03 15:36:45', NULL, NULL, 2, 1),
            (1, 'game1', 'soccer-world-cup', 10, 'sports', 3, 30, 1, '2017-08-03 15:36:45', NULL, NULL, 6, 3),
            (2, 'game2', 'chemistry', 10, 'science', 2, 20, 1, '2017-09-13 21:40:05', NULL, NULL, 4, 2),
            (3, 'game3', 'social_sciences', 10, 'social_sciences', 4, 20, 1, '2017-09-20 08:19:32', NULL, NULL, 8, 4),
            (4, 'game4', 'sciences', 10, 'sciences', 2, 20, 1, '2017-09-13 21:40:05', NULL, NULL, 4, 2),
            (5, 'game5', 'soccer-world-cup', 10, 'sports', 2, 30, 1, '2017-09-20 08:19:32', NULL, NULL, 4, 2),
            (6, 'game6', 'football', 10, 'science', 5, 50, 1, '2017-09-13 21:40:05', NULL, NULL, 10, 5),
            (7, 'game7', 'europe-capitals', 10, 'other', 1, 10, 1, '2017-09-20 08:19:32', NULL, NULL, 2, 1),
            (8, 'game8', 'pop-art', 10, 'other', 2, 20, 1, '2017-08-03 15:36:45', NULL, NULL, 4, 2),
            (9, 'game9', 'world-capitals', 10, 'other', 1, 10, 1, '2017-09-13 21:40:05', NULL, NULL, 2, 1),
           # (10, 'game10', 'astronomy', 10, 'other', 3, 30, 1, '2017-09-20 08:19:32', NULL, NULL, 6, 3)
           ]

        aa = {}
        for game in range(len(sql_data)):
            print sql_data[game]
            aa[str(game)] ={}
            aa[str(game)]['game_room_id'] = float(sql_data[game][0])
            aa[str(game)]['game_room_name'] = sql_data[game][1]
            aa[str(game)]['small_blind'] = float(sql_data[game][12])
            aa[str(game)]['big_blind'] = float(sql_data[game][11])
            aa[str(game)]['max_buy_in'] = float(sql_data[game][6])
            aa[str(game)]['min_buy_in'] = float(sql_data[game][5])
            aa[str(game)]['game_theme'] = sql_data[game][4]
            aa[str(game)]['game_category'] = sql_data[game][2]
            aa[str(game)]['max_players'] = sql_data[game][3]
            aa[str(game)]['current_max_bet'] = sql_data[game][11]
            aa[str(game)]['pot_amount'] = 0
            aa[str(game)]['player_bet'] = {}
            aa[str(game)]['total_amount'] = {}
            aa[str(game)]['clients'] = []
            aa[str(game)]['idle_gameroom'] = True
        print aa
    #ini1tial redis initilisation (to be made dynamic later)
        # aa = {
        #     "1":{'game_room_name': u'game1', 'small_blind': 20, 'big_blind': 40, 'max_buy_in': 80, 'game_theme': u'sports', 'game_room_id': 1L, 'game_category': u'soccer-world-cup', 'max_players': 10, 'min_buy_in': 20,'current_max_bet':40,'pot_amount':0,'player_bet': {},'total_amount':{},'clients':[], 'idle_gameroom' : True},
        #     "2":{'game_room_name': u'game2', 'small_blind': 20, 'big_blind': 40, 'max_buy_in': 1000, 'game_theme': u'Sports', 'game_room_id': 2L, 'game_category': u'tennis', 'max_players': 10, 'min_buy_in': 200,'current_max_bet':40,'pot_amount':0,'player_bet': {},'total_amount':{},'clients':[], 'idle_gameroom' : True},
        #     "3":{'game_room_name': u'game3', 'small_blind': 20, 'big_blind': 40, 'max_buy_in': 500, 'game_theme': u'social_science', 'game_room_id': 3L, 'game_category': u'social_science', 'max_players': 10, 'min_buy_in': 100,'current_max_bet':40,'pot_amount':0,'player_bet': {},'total_amount':{},'clients':[], 'idle_gameroom' : True},
        #     "4":{'game_room_name': u'game4', 'small_blind': 2, 'big_blind': 4, 'max_buy_in': 100, 'game_theme': u'sports', 'game_room_id': 4L, 'game_category': u'football', 'max_players': 10, 'min_buy_in': 25,'current_max_bet':4,'pot_amount':0,'player_bet': {},'total_amount':{},'clients':[], 'idle_gameroom' : True},
        #     "5":{'game_room_name': u'game5', 'small_blind': 5, 'big_blind': 10, 'max_buy_in': 100, 'game_theme': u'economics', 'game_room_id': 5L, 'game_category': u'football', 'max_players': 10, 'min_buy_in': 25,'current_max_bet':10,'pot_amount':0,'player_bet': {},'total_amount':{},'clients':[], 'idle_gameroom' : True},
        #     "6":{'game_room_name': u'game6', 'small_blind': 10, 'big_blind': 20, 'max_buy_in': 200, 'game_theme': u'sports', 'game_room_id': 6L, 'game_category': u'football', 'max_players': 10, 'min_buy_in': 50,'current_max_bet':20,'pot_amount':0,'player_bet': {},'total_amount':{},'clients':[], 'idle_gameroom' : True},
        #     "7":{'game_room_name': u'game7', 'small_blind': 15, 'big_blind': 30, 'max_buy_in': 300, 'game_theme': u'sports', 'game_room_id': 7L, 'game_category': u'football', 'max_players': 10, 'min_buy_in': 100,'current_max_bet':30,'pot_amount':0,'player_bet': {},'total_amount':{},'clients':[], 'idle_gameroom' : True},
        #     "8":{'game_room_name': u'game8', 'small_blind': 25, 'big_blind': 50, 'max_buy_in': 500, 'game_theme': u'economics', 'game_room_id': 8L, 'game_category': u'football', 'max_players': 10, 'min_buy_in': 100,'current_max_bet':50,'pot_amount':0,'player_bet': {},'total_amount':{},'clients':[], 'idle_gameroom' : True},
        #     "9":{'game_room_name': u'game9', 'small_blind': 50, 'big_blind': 100, 'max_buy_in': 500, 'game_theme': u'science', 'game_room_id': 9L, 'game_category': u'football', 'max_players': 10, 'min_buy_in': 100,'current_max_bet':100,'pot_amount':0,'player_bet': {},'total_amount':{},'clients':[], 'idle_gameroom' : True},
        #     "10":{'game_room_name': u'game10', 'small_blind': 100, 'big_blind': 200, 'max_buy_in': 1000, 'game_theme': u'Sports', 'game_room_id': 10L, 'game_category': u'football', 'max_players': 10, 'min_buy_in': 500,'current_max_bet':200,'pot_amount':0,'player_bet': {},'total_amount':{},'clients':[], 'idle_gameroom' : True}
        # }

        oo = {
            '0': {'seat_8': '-1', 'seat_9': '-1', 'seat_10': '-1', 'seat_4': '-1', 'seat_5': '-1', 'seat_6': '-1', 'seat_7': '-1', 'seat_1': '-1', 'seat_2': '-1', 'seat_3': '-1'},
            '1': {'seat_8': '-1', 'seat_9': '-1', 'seat_10': '-1', 'seat_4': '-1', 'seat_5': '-1', 'seat_6': '-1', 'seat_7': '-1', 'seat_1': '-1', 'seat_2': '-1', 'seat_3': '-1'},
            '2': {'seat_8': '-1', 'seat_9': '-1', 'seat_10': '-1', 'seat_4': '-1', 'seat_5': '-1', 'seat_6': '-1', 'seat_7': '-1', 'seat_1': '-1', 'seat_2': '-1', 'seat_3': '-1'},
            '3': {'seat_8': '-1', 'seat_9': '-1', 'seat_10': '-1', 'seat_4': '-1', 'seat_5': '-1', 'seat_6': '-1', 'seat_7': '-1', 'seat_1': '-1', 'seat_2': '-1', 'seat_3': '-1'},
            '4': {'seat_8': '-1', 'seat_9': '-1', 'seat_10': '-1', 'seat_4': '-1', 'seat_5': '-1', 'seat_6': '-1', 'seat_7': '-1', 'seat_1': '-1', 'seat_2': '-1', 'seat_3': '-1'},
            '5': {'seat_8': '-1', 'seat_9': '-1', 'seat_10': '-1', 'seat_4': '-1', 'seat_5': '-1', 'seat_6': '-1', 'seat_7': '-1', 'seat_1': '-1', 'seat_2': '-1', 'seat_3': '-1'},
            '6': {'seat_8': '-1', 'seat_9': '-1', 'seat_10': '-1', 'seat_4': '-1', 'seat_5': '-1', 'seat_6': '-1', 'seat_7': '-1', 'seat_1': '-1', 'seat_2': '-1', 'seat_3': '-1'},
            '7': {'seat_8': '-1', 'seat_9': '-1', 'seat_10': '-1', 'seat_4': '-1', 'seat_5': '-1', 'seat_6': '-1', 'seat_7': '-1', 'seat_1': '-1', 'seat_2': '-1', 'seat_3': '-1'},
            '8': {'seat_8': '-1', 'seat_9': '-1', 'seat_10': '-1', 'seat_4': '-1', 'seat_5': '-1', 'seat_6': '-1', 'seat_7': '-1', 'seat_1': '-1', 'seat_2': '-1', 'seat_3': '-1'},
            '9': {'seat_8': '-1', 'seat_9': '-1', 'seat_10': '-1', 'seat_4': '-1', 'seat_5': '-1', 'seat_6': '-1', 'seat_7': '-1', 'seat_1': '-1', 'seat_2': '-1', 'seat_3': '-1'},
            '10': {'seat_8': '-1', 'seat_9': '-1', 'seat_10': '-1', 'seat_4': '-1', 'seat_5': '-1', 'seat_6': '-1', 'seat_7': '-1', 'seat_1': '-1', 'seat_2': '-1', 'seat_3': '-1'},
            '11': {'seat_8': '-1', 'seat_9': '-1', 'seat_10': '-1', 'seat_4': '-1', 'seat_5': '-1', 'seat_6': '-1', 'seat_7': '-1', 'seat_1': '-1', 'seat_2': '-1', 'seat_3': '-1'},
            '12': {'seat_8': '-1', 'seat_9': '-1', 'seat_10': '-1', 'seat_4': '-1', 'seat_5': '-1', 'seat_6': '-1', 'seat_7': '-1', 'seat_1': '-1', 'seat_2': '-1', 'seat_3': '-1'},
            '13': {'seat_8': '-1', 'seat_9': '-1', 'seat_10': '-1', 'seat_4': '-1', 'seat_5': '-1', 'seat_6': '-1', 'seat_7': '-1', 'seat_1': '-1', 'seat_2': '-1', 'seat_3': '-1'}
        }

        ss = {
            "1": {},
            "2": {},
            "3": {},
            "4": {},
            "5": {},
            "6": {},
            "7": {},
            "8": {},
            "9": {},
            "10": {},
            "11": {},
            "12": {},
            "13": {}
        }

        ll = {
            "game3": "3",
            "game2": "2",
            "game1": "1",
            "game4": "4",
            "game5": "5",
            "game6": "6",
            "game7": "7",
            "game8": "8",
            "game9": "9",
            "game10": "10",
            "game11": "11",
            "game12": "12",
            "game13": "13"
        }

        r.set('active_games', json.dumps(ll))
        r.set('right_ans', json.dumps(ss))
        r.set('active_set',json.dumps(aa))
        r.set('sitted_clients',json.dumps(oo))
        # for profile photos
        r.set('profile', json.dumps({}))
        #redis initialisation ends here
