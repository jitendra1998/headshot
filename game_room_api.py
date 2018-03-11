from routes import *
from datetime import datetime
import time
from mysql_configure import MYSQLConfiguration
from common import *
from queries import SQLqueries
from messages import errors
from messages import success
import redis
import json
from random import randint
from helperfunctions import *
import requests
from banner_api import BannerStats, BannerDict
from mod_func import *

r = redis.StrictRedis(host='localhost', db=4)

query_obj = SQLqueries()
error_obj = errors()
success_obj = success()
#host ='52.187.112.27'
#host = '114.79.139.54'
#host = 'ec2-18-220-209-33.us-east-2.compute.amazonaws.com'
# host = 'localhost'
host = '52.163.123.180'
sit_out_on_wsclose = True
global_id = None

#global round_no
#global ans_submit
#global req
#global idle_gameroom
#global all_in_list
obj_help = HelpingFunctions()

class Game_room_showall(CommonBaseHandler):

    def get(self):
        # game_room_id = self.get_secure_cookie("game_room_id")
        # if game_room_id:
        #     self.clear_cookie("game_room_id")
        # self.set_headers()
        response_data = ""
        #look if its used or not
        dict_user = json.loads(r.get(('user_session').decode('utf-8')))
        # user_id = self.get_argument("user_id",default="",strip=False)
        #check username in user_session
        if self.redis_session_check(self.get_secure_cookie("qc_user")):
            #changes on active_games table
            game_ids = json.loads(r.get('active_set').decode('utf-8'))
            game_data = []
            if game_ids:#use list comprehension

                # get active_gamerooms list as [id,]
                active_gamerooms=game_ids.keys()

                players = {}
                # fetch game_data for each id in active_gamerooms
                for gameroom in active_gamerooms:
                    game_data.extend(self.get_game_data(gameroom))
                    sitted_clients = json.loads(r.get('sitted_clients'))[gameroom]
                    player = 0
                    for client in sitted_clients.values():
                        if client != '-1':
                            player=player+1
                    players[gameroom] = player

                player_id = json.loads(r.get('user_session'))[self.get_secure_cookie("qc_user")]

                wallet_operation_obj = WriteData()
                user_data_current = wallet_operation_obj.get_user_data(player_id)
                balance = user_data_current[0]['virtual_money']
                profile_photo = self.get_user_data(player_id)[0]['profile_image']
                if profile_photo is None:
                    profile_photo = "profile-default.png"

                self.render("join_game.html", host=host,player_id=player_id, user_name = self.get_secure_cookie("qc_user"), user_balance = balance, Active_Game_Rooms = game_data,players=players, profile_photo= profile_photo)
            else:
                response_data = json.dumps({
                    'error': {
                        'code': error_obj.error_code_not_found,
                        'message': error_obj.error_no_active_games
                    }
                })
        else:
            response_data = json.dumps({
                'error': {
                    'code': error_obj.error_code_unauthorized,
                    'message': error_obj.error_message_login
                }
            })

    def post(self):
        # no sit out when going from lobby to gameroom
        global sit_out_on_wsclose
        sit_out_on_wsclose = False

        self.set_headers()
        Game_Room_id = self.get_argument("Game_Room_id")
        user_name = self.get_secure_cookie("qc_user")
        seat = self.get_argument("seat")
        
        #set cookie to save game_room_id
        self.set_secure_cookie("game_room_id", Game_Room_id)

        # passing user_buy_in value to gameroom
        buy_in = self.get_argument("buy_in")
        active_set = json.loads(r.get('active_set').decode('utf-8'))
        usr = json.loads(r.get('user_session').encode('utf-8'))
        player_id = usr[user_name]
        active_set[Game_Room_id]['total_amount'][player_id] = buy_in
        r.set('active_set', json.dumps(active_set))

        # set gameroom record in last_session
        session_log = json.loads(r.get('last_session'))
        if str(Game_Room_id) in session_log[player_id]['gamerooms'].values():
            old_buy_in = session_log[player_id]['gamerooms'][str(Game_Room_id)]['buy-in']
            old_earnings = session_log[player_id]['gamerooms'][str(Game_Room_id)]['earnings']
            session_log[player_id]['gamerooms'][str(Game_Room_id)] =  {
                'buy-in': str(float(old_buy_in) + float(buy_in)),
                'earnings': str(float(old_earnings) - float(buy_in))
            }
        else:
            session_log[player_id]['gamerooms'][str(Game_Room_id)] =  {
                'buy-in': buy_in,
                'earnings': str(0 - float(buy_in))
            }
        r.set('last_session', json.dumps(session_log))

        # deduct buy-ins
        wallet_operation_obj = WriteData()
        user_balance = wallet_operation_obj.get_user_data(player_id)[0]['virtual_money']
        wallet_operation_obj.append_player_balance(float(player_id),float(user_balance)-float(buy_in))

        response_data = ""
        response_data = json.dumps({
            'Game_Info': {
                'Game_Room_id': Game_Room_id,
                'User_Name': user_name
            }
        })
        self.redirect('/user/view_games/Game_Room/' + Game_Room_id + "/" + seat)


class Game_Room(CommonBaseHandler):

    @tornado.web.asynchronous
    def get(self,game_room_id,seat):
        user_name = self.get_secure_cookie("qc_user")
        player_id = json.loads(r.get('user_session').decode('utf-8'))[user_name]
        user_data = []
        user_data.extend(self.get_user_data(player_id))

        # add eyeball count to banner
        banner = BannerStats('test1')
        banner.update_banner(viewed_by=str(player_id))
        
        
        self.render("game_page.html", host=host, game_room_id=game_room_id, player_id=player_id, user_name = user_name, seat = seat)

    def post(self, game_room_id, seat):
        # increase click-count of banner
        banner = BannerStats('test1')
        banner.update_banner(clicked_by =str(self.get_argument("click")))

clients = {}
client_gameplay = []
player_seq =[]
sitted_clients_template = {'seat_1': '-1', 'seat_2': '-1','seat_3': '-1','seat_4': '-1','seat_5': '-1','seat_6': '-1','seat_7': '-1','seat_8': '-1','seat_9': '-1','seat_10': '-1'}
#round_no =2
#req = {}
ans_submit = 0
#all_in_list=[]
#idle_gameroom = True
waiting_for = ''
        
obj = GameActions()
class WebSocketHandler1(tornado.websocket.WebSocketHandler,CommonBaseHandler): 
    
    def check_origin(self, origin):
        return True

    def open(self, game_room_id):
        # global idle_gameroom
        global sit_out_on_wsclose
        sit_out_on_wsclose = True

        tmp = []

        #add the user to the active_players table once the websocket opens for the particular user
        player_id = json.loads(r.get('user_session').encode('utf-8'))[self.get_secure_cookie('qc_user')]
        if r.get('active_players'):
            tmp_str = json.loads(r.get('active_players').decode('utf-8'))
            if not tmp_str.has_key(game_room_id):
                tmp_str[game_room_id] = []
                
            if player_id not in tmp_str[game_room_id]:
                tmp_str[game_room_id].extend(player_id)           
            r.set('active_players', json.dumps(tmp_str))
        else:
            pid =[]
            pid.append(player_id)
            r.set('active_players', json.dumps({game_room_id : pid})) 
#        opp = json.loads(r.get('active_set'))
#        game_room_id = self.get_secure_cookie("game_room_id")
#        clients = opp[str(game_room_id)]['clients']
#        clients.append(self)
#        opp[str(game_room_id)]['clients'] = clients
#        r.set('active_set',json.dumps(opp))
        print clients,"This on open :--> ", game_room_id
        for key in clients.keys():
            if str(player_id) in clients[key]:
                clients[key].pop(str(player_id))
        if str(game_room_id) in clients:
            clients[str(game_room_id)][str(player_id)] = self
        elif str(game_room_id) != 'undefined':
            clients[str(game_room_id)] = {}
            clients[str(game_room_id)][str(player_id)] = self
        print clients,"This on open AFTER:--> ", game_room_id
        
        #representation of sitted clients
        # sitted_clients = json.loads(r.get('sitted_clients'))[str(game_room_id)]
        kk = obj_help.redis_fetch('active_set')[str(game_room_id)]
        # call_amount = kk['current_max_bet']

        # send update message on websocket
        pot_amount = kk['pot_amount']
        pot_msg = {}
        pot_msg['game_key'] = 'update_pot'
        pot_msg['pot_amount'] = pot_amount
        for client in clients[str(game_room_id)].values():
            client.write_message(json.dumps(pot_msg))

        #defining total amount
        total_amount = {}
        usr = json.loads(r.get('user_session').encode('utf-8'))
        usr_ult = {}
        for i,j in usr.iteritems():
            usr_ult[j] = i
        for key,value in kk['total_amount'].iteritems():
            if usr_ult[key] in total_amount:
                total_amount[usr_ult[key]] = value

        # load profile photos for sitted clients
        user_amount = {}
        sitted_clients = json.loads(r.get('sitted_clients'))[str(game_room_id)]
        for ids in kk['total_amount']:
            if ids in usr_ult:
                for seat in sitted_clients:
                    if usr_ult[ids] == sitted_clients[seat]:
                        user_amount[seat] = kk['total_amount'][ids]
        profile_dict = json.loads(r.get('profile'))
        if str(game_room_id) in profile_dict.keys():
            profile_dict = json.loads(r.get('profile'))[str(game_room_id)]
        else:
            profile_dict = {}

        balance = {}
        wallet_operation_obj = WriteData()
        # udate wallets initially
        total_amount_dict = json.loads(r.get('active_set'))[str(game_room_id)]['total_amount']
        if player_id not in total_amount_dict:
            balance[player_id] = wallet_operation_obj.get_user_data(player_id)[0]['virtual_money']
        for player in total_amount_dict:
            balance[player] = float(wallet_operation_obj.get_user_data(player)[0]['virtual_money']) + float(total_amount_dict[player])
        # send update message on websocket
        msg = {}
        msg['game_key'] = 'update_wallet'
        msg['balance'] = balance
        for client in clients[str(game_room_id)].values():
            client.write_message(json.dumps(msg))

        mess = {
            'game_key': "10",
            'profile': profile_dict,
            'sitted_clients': json.loads(r.get('sitted_clients'))[str(game_room_id)],
            'total_amount': user_amount,
        }

        for client in clients[str(game_room_id)].values():
            client.write_message(mess)


        # check for ad banners
        banner_dict = BannerDict()
        banners = banner_dict.get_banner_dict()
        for banner in banners:
            if str(game_room_id) in banners[banner]['gamerooms']:
                this_banner = BannerStats(banner)
                this_banner = this_banner.get_banner_stats()
                # send ads position on websocket
                message_for_banner = {
                    'game_key': 'banner_check',
                    'position': banners[banner]['gamerooms'][str(game_room_id)],
                    'link': this_banner['link']
                }
                for client in clients[str(game_room_id)].values():
                    client.write_message(json.dumps(message_for_banner))

        # # check no of players in gameroom
        #
        # sitted_clients = json.loads(r.get('sitted_clients'))
        # sitted_clients_for_gameroom = sitted_clients[str(game_room_id)]
        # this_gameroom_active_players = []
        # for seat in sitted_clients_for_gameroom:
        #     if sitted_clients_for_gameroom[seat] != '-1':
        #         this_gameroom_active_players.append(seat)
        # if len(this_gameroom_active_players) == 2:
        idle_gameroom = json.loads(r.get('active_set'))[str(game_room_id)]['idle_gameroom']
        if len(json.loads(r.get('active_set'))[str(game_room_id)]['total_amount']) > 1 and idle_gameroom:

            # start the game
            automated_start = {
                'user_name': 'admin',
                'game_room_id': str(game_room_id)
                }
            obj.start_set(json.dumps(automated_start), clients)

    def on_message(self, message):
        global waiting_for
#        global idle_gameroom
#        global req
        mass_dec = json.loads(message)
        
        global ans_submit
#        global round_no
#        global all_in_list
        #game_key = 'nil'
        game_key = mass_dec['game_key']
        user_name = self.get_secure_cookie("qc_user")

        # listen for self.rebuyin on websocket
        if game_key == 'rebuyin':
            obj.rebuyin(mass_dec, clients)
        elif game_key == '1':
            mess = json.dumps(mass_dec)
            for client in clients[str(mass_dec['game_room_id'])].values():
                client.write_message(mess)
        elif game_key == '2':
            global global_id
            global_id = str(mass_dec['game_room_id'])
            obj.sit_here_func(mass_dec, clients)
            
        elif game_key == '3':
#            client_gameplay.remove(self)
            obj.sit_out(json.dumps(mass_dec), clients)
            
        elif game_key == '4':
#            all_in_list = []
            #this calls the obj.start_set function which initializes all the redis tables and the required game data
            print clients,"This on START SET:"
            obj.start_set(message,clients)
        elif game_key == '5':

            print "here at 5"
            obj.game_action(mass_dec,clients)
                    
        elif game_key =='7':
            obj.submit_ans(mass_dec,clients)
            
                
        elif game_key=='12':
            mass_dec['game_key'] ='12'
            for client in clients[str(mass_dec['game_room_id'])].values():
                    client.write_message(json.dumps(mass_dec))
            obj_help.redis_init_tables()

    def on_close(self):
       # opp = json.loads(r.get('active_set'))
       # game_room_id = self.get_secure_cookie("game_room_id")
       # clients = opp[str(game_room_id)]['clients']
       # print clients, "this on close:-->", game_room_id
       # if self in clients[str(game_room_id)]:
       #     clients[str(game_room_id)].remove(self)
       # print clients, "this on close AFTER:-->", game_room_id
        global sit_out_on_wsclose
        global waiting_for
       # global round_no
       # global idle_gameroom
        
        user_name = self.get_secure_cookie("qc_user")
        player_id = json.loads(r.get('user_session').encode('utf-8'))[self.get_secure_cookie('qc_user')]
        game_room_id_cookie = self.get_secure_cookie("game_room_id")
        print "This on close:",clients
        if clients and game_room_id_cookie:
            if self in clients[str(game_room_id_cookie)].values():
                clients[str(game_room_id_cookie)].pop(str(player_id))
            else:
                pass
        else:
            pass
        print "This on close AFTER: ", clients


        if sit_out_on_wsclose:
            #call sitout on left user
            
            # usr = json.loads(r.get('user_session'))
            # player_id = usr[user_name]

            # if player has a seat in game sit him out
            global global_id
            if global_id is not None:
                game_room_id = global_id
                print "inside slobal id"
                # game_room_id = self.get_secure_cookie("game_room_id")
                # if game_room_id:
                seat_no = ""
                #sitted_clients
                sitted_clients_tmp = json.loads(r.get('sitted_clients'))[str(game_room_id)]
                print sitted_clients_tmp
                for key,value in sitted_clients_tmp.iteritems():
                    print key,value
                    if value == user_name:
                        seat_no = key
                        
                        if seat_no == waiting_for:
                            print "seat == waiting for::"
                            usr = json.loads(r.get('user_session').encode('utf-8'))
                            player_id = usr[user_name]
                            player_seq1 = obj_help.redis_fetch('shuffled_active_players')[str(game_room_id)]
                            usr_ult = {}
                            ind1 = 0  # next player id
                            ind2 = 0  # next player index
                            ind3 = 0  # current player index
                            for i, j in usr.iteritems():
                                usr_ult[j] = i
                            sitted_clients = json.loads(r.get('sitted_clients'))[str(game_room_id)]
                            mass_dec = {}
                            for ind, val in enumerate(player_seq1):
                                if val == usr[user_name]:
                                    ind2 = (ind + 1) % len(player_seq1)
                                    ind1 = player_seq1[ind2]
                                    for seat, u_name in sitted_clients.iteritems():
                                        if u_name != '-1':
                                            if ind1 == usr[u_name]:
                                                mass_dec['curr_seat_no'] = seat
                                                waiting_for = mass_dec['curr_seat_no']
                                                ind3 = ind
                            # no action if player is all_in
                            all_in_list = json.loads(r.get('active_set'))[game_room_id]['all_in_list']
                            if player_id not in all_in_list:
                                obj_help.fold(player_id, game_room_id)
                                player_seq1 = obj_help.redis_fetch('shuffled_active_players')[str(game_room_id)]
                                if len(player_seq1) == 1:
                                    opp  = json.loads(r.get('active_set'))
                                    opp[str(game_room_id)]['idle_gameroom'] = True
                                    r.set('active_set', json.dumps(opp))
                                    
                                    obj_help.divide_cash_len(str(game_room_id), player_seq1[0])

                                    mess = {u'opt': [u'nil', u'nil', u'nil', u'nil'], u'answer_time': u'nil',
                                            u'game_key': u'3', u'seat_no': seat_no, u'ans': u'nil', u'action': u'nil',
                                            u'game_room_id': game_room_id, u'message': u'has left seat_3',
                                            u'user_name': user_name, u'con_id': u'nil', u'dealer_seat': u'nil',
                                            u'con': u'nil'}
                                    obj.sit_out(json.dumps(mess), clients)

                                    # start the game
                                    automated_start = {
                                        'user_name': 'admin',
                                        'game_room_id': str(game_room_id)
                                    }
                                    
                                    obj.start_set(json.dumps(automated_start), clients)
                                else:
                                    # updates for front end
                                    active_set = json.loads(r.get('active_set'))[game_room_id]
                                    mass_dec['game_key'] = '5'
                                    mass_dec['seat_no'] = seat_no
                                    mass_dec['pot_amount'] = active_set['pot_amount']
                                    mass_dec['user_amount'] = 0
                                    mass_dec['call_amount'] = float(active_set['current_max_bet']) - float(
                                        active_set['player_bet'][ind1])
                                    mass_dec['bet_amount'] = 2 * float(active_set['current_max_bet']) - float(
                                        active_set['player_bet'][ind1])
                                    mass_dec['next_user_amount'] = active_set['total_amount'][ind1]
                                    round_no = r.get('active_set')[str(game_room_id)]['round_no']
                                    if round_no < 5:
                                        for client in clients[str(game_room_id)].values():
                                            client.write_message(json.dumps(mass_dec))
                        else:
                            mess = {u'opt': [u'nil', u'nil', u'nil', u'nil'], u'answer_time': u'nil',
                                    u'game_key': u'3', u'seat_no': seat_no, u'ans': u'nil', u'action': u'nil',
                                    u'game_room_id': game_room_id, u'message': u'has left seat_3',
                                    u'user_name': user_name, u'con_id': u'nil', u'dealer_seat': u'nil',
                                    u'con': u'nil'}
                            obj.sit_out(json.dumps(mess), clients)

                            player_seq1 = obj_help.redis_fetch('shuffled_active_players')[str(game_room_id)]
                            if len(player_seq1) == 1:
                                opp = json.loads(r.get('active_set'))
                                opp[str(game_room_id)]['idle_gameroom'] = True
                                r.set('active_set', json.dumps(opp))
                                
                                hide_button_message = {
                                    'game_key':'hide_buttons',
                                    'game_room_id': str(game_room_id)
                                }
                                for client in clients[str(game_room_id)].values():
                                    try:
                                        client.write_message(json.dumps(hide_button_message))
                                    except Exception as e:
                                        pass
                                obj_help.divide_cash_len(str(game_room_id), player_seq1[0])

                                # start the game
                                automated_start = {
                                    'user_name': 'admin',
                                    'game_room_id': str(game_room_id)
                                }
                                print "IT REACHED HERE: -->"
                                obj.start_set(json.dumps(automated_start), clients)

