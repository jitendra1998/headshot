from helperfunctions import *
from common import *
from mysql_configure import MYSQLConfiguration
from banner_api import BannerStats, BannerDict
from game_room_api import *
import math

import random
import redis as rd
import json

r = rd.StrictRedis('localhost',db=4)
red = rd.StrictRedis('localhost',db=4)
req = {}
obj_help = HelpingFunctions()
#call this function after every round is completed, it's supposed to initialize the pot_amount, select dealer, get question
class GameActions(object):

    def start_set(self, message, clients):
    
        round_no =2
        global req 
        req = {}
    #    ans_submit =0
    #    print message,type(message)
        
        if isinstance(message,str):
            mass_dec = json.loads(message)
        else:
            mass_dec = message
        idle_gameroom = json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]['idle_gameroom']
        
        player_list =[]
        usr = json.loads(r.get('user_session').encode('utf-8'))
    #    clients = json.loads('active_set')[str(mass_dec['game_room_id'])]['clients']
        oclients = clients
        clients = clients[str(mass_dec['game_room_id'])].values()
    #    all_in_list=[]
    
        # check for ad banners
        banner_dict = BannerDict()
        banners = banner_dict.get_banner_dict()
        for banner in banners:
            if str(mass_dec['game_room_id']) in banners[banner]['gamerooms']:
                this_banner = BannerStats(banner)
                this_banner = this_banner.get_banner_stats()
                # send ads position on websocket
                message_for_banner = {
                    'game_key':'banner_check',
                    'position': banners[banner]['gamerooms'][str(mass_dec['game_room_id'])],
                    'link': this_banner['link']
                }
                for client in clients:
                    client.write_message(json.dumps(message_for_banner))
    
        usr_ult = {}
        for i, j in usr.iteritems():
            usr_ult[j] = i
    
        #create a random player sequence, with the sitted player data
        sitted_clients = json.loads(r.get('sitted_clients'))[str(mass_dec['game_room_id'])]
        for key in sitted_clients:
            if sitted_clients[key]!='-1':
                for i,j in usr.iteritems():
                    if i == sitted_clients[key]:
                        player_list.append(j)
        active_set = json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]
        player_list = [ele for ele in player_list if ele in active_set['total_amount'].keys()]
        # if len(player_list) > 1:
        print idle_gameroom, len(json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]['total_amount'])
        if len(json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]['total_amount'])>1 and idle_gameroom:
                                   
    #        idle_gameroom = False
            opp  = json.loads(r.get('active_set'))
            opp[str(mass_dec['game_room_id'])]['idle_gameroom'] = False
            r.set('active_set', json.dumps(opp))
                                   
            obj_help.select_player(player_list,str(mass_dec['game_room_id']))
            player_seq = obj_help.redis_fetch('shuffled_active_players')
            obj_help.start_game(str(mass_dec['game_room_id']))
            for i,j in sitted_clients.iteritems():
                for k,l in usr.iteritems():
                    if player_seq[str(mass_dec['game_room_id'])][3%len(player_seq[str(mass_dec['game_room_id'])])] == l:
                        if k==j :
                            mass_dec['dealer_seat'] = i
                            mass_dec['message'] = j

            mass_dec['game_key'] = '4'
            mass_dec['question_no'] = randint(1,1000)

            usr = json.loads(r.get('user_session').encode('utf-8'))
            active_set = json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]
            call_amount = float(active_set['current_max_bet']) - float(active_set['player_bet'][usr[sitted_clients[mass_dec['dealer_seat']]]])
            bet_amount = 2 * float(active_set['current_max_bet']) - float(active_set['player_bet'][usr[sitted_clients[mass_dec['dealer_seat']]]])

            #defining total amount
            total_amount = {}
            for key,value in active_set['total_amount'].iteritems():
                total_amount[usr_ult[key]] = value

            # updating call and bet amount
            mass_dec['call_amount'] = call_amount
            mass_dec['bet_amount'] = bet_amount
            mass_dec['next_user_amount'] = active_set['total_amount'][usr[sitted_clients[mass_dec['dealer_seat']]]]
            # put profile photos for sitted clients
            profile_dict = json.loads(r.get('profile'))
            user_amount = {}
            for ids in active_set['total_amount']:
                if ids in usr_ult:
                    for seat in sitted_clients:
                        if usr_ult[ids] == sitted_clients[seat]:
                                user_amount[seat] = active_set['total_amount'][ids]
            print user_amount ,"THis is user-amount"
            if str(mass_dec['game_room_id']) in profile_dict.keys():
                profile_dict = json.loads(r.get('profile'))[str(mass_dec['game_room_id'])]
            else:
                profile_dict = {}

            active_player_list = obj_help.redis_fetch('shuffled_active_players')[str(mass_dec['game_room_id'])]
            print 'This is sitted Clients'
            print sitted_clients.keys()[sitted_clients.values().index(usr_ult[active_player_list[1%len(active_player_list)]])]
            print 'This is sitted Clients'
            sb_amount =  obj_help.redis_fetch('active_set')[str(mass_dec['game_room_id'])]['small_blind']
            small_blind = sitted_clients.keys()[sitted_clients.values().index(usr_ult[active_player_list[1%len(active_player_list)]])]
            bb_amount =  obj_help.redis_fetch('active_set')[str(mass_dec['game_room_id'])]['big_blind']
            big_blind = sitted_clients.keys()[sitted_clients.values().index(usr_ult[active_player_list[2 % len(active_player_list)]])]
            mass_dec['small_blind'] = small_blind
            mass_dec['sb_amount'] = sb_amount
            mass_dec['big_blind'] = big_blind
            mass_dec['bb_amount'] = bb_amount
            mass_dec['user_amount']= user_amount
            mess = {
                'game_key': "10",
                'profile': profile_dict,
                'sitted_clients': sitted_clients,
                'total_amount': total_amount,
                'small_blind':small_blind,
                'big_blind':big_blind,
                'sb_amount':sb_amount,
                'bb_amount':bb_amount,
                'user_amount': user_amount

            }

            update_call_bet_message = {
                'game_key': 'update_call_bet',
                'call_amount': call_amount,
                'bet_amount': bet_amount
            }

            for client in clients:
                client.write_message(json.dumps(mass_dec))
                client.write_message(json.dumps(mess))
                client.write_message(json.dumps(update_call_bet_message))

            game_room_id = mass_dec['game_room_id']
            #get a random question based on theme and sitted player data
            print active_set, 'This is mass Dec'
            req_success =False
            while req_success == False:
                req = json.loads(requests.post('http://localhost:8088/question', data = {'Game_Room_id': json.dumps({game_room_id:player_seq}), 'theme': active_set['game_category'] }).text)
    #            req = json.loads(req.text)
                if str("success") in req:
                    req_success = True

            opp = json.loads(r.get('active_set'))
            opp[str(mass_dec['game_room_id'])]['req'] = req
            opp[str(mass_dec['game_room_id'])]['all_in_list'] = []
            opp[str(mass_dec['game_room_id'])]['round_no'] = round_no
            opp[str(mass_dec['game_room_id'])]['ans_submit'] = 0
            r.set('active_set',json.dumps(opp))
            # r.set('question_data', json.dumps(req))


            #write the first hint once the game starts
            mass_dec['game_key'] = '6'
            mass_dec['con_id'] = 'cat_1'
            mass_dec['con'] = req['success']['data']['d1'][1]
            active_set = json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]

            mass_dec['pot_amount'] = active_set['pot_amount']

            for client in clients:
                client.write_message(json.dumps(mass_dec))

            active_player_list = obj_help.redis_fetch('shuffled_active_players')[str(mass_dec['game_room_id'])]
            small_blind_notification = json.dumps({
                'game_key': '1',
                'user_name': usr_ult[active_player_list[1%len(active_player_list)]],
                'message': "Played Small Blind " + str(active_set['small_blind']) + u"\u20ac"
            })
            big_blind_notification = json.dumps({
                'game_key': '1',
                'user_name': usr_ult[active_player_list[2%len(active_player_list)]],
                'message':"Played Big Blind " + str(active_set['big_blind']) + u"\u20ac"
            })
            for client in clients:
                client.write_message(small_blind_notification)
                client.write_message(big_blind_notification)

        else:
    #        idle_gameroom = True
            print "this is waiting"
            opp  = json.loads(r.get('active_set'))
            opp[str(mass_dec['game_room_id'])]['idle_gameroom'] = True
            r.set('active_set', json.dumps(opp))

            waiting_message = json.dumps({
                'game_key': '1',
                'user_name': "Waiting for players",
                'message':"to join"
            })
            for client in clients:
                client.write_message(waiting_message)

            if len(json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]['total_amount'])>1:
                self.start_set(message, oclients)

    #self.sit_out modular function
    def sit_out(self, message, clients):
        #self.self.sit_out init
        mass_dec = json.loads(message)
    #    clients = json.loads('active_set')[str(mass_dec['game_room_id'])]['clients']
        clients = clients[str(mass_dec['game_room_id'])].values()
        global global_id
        global_id = None

        #when a players sits out, information is again updated in redis active_set table, balance is written in sql and total_amount and player_keys are removed for the respective user
        active_set = json.loads(r.get('active_set').decode('utf-8'))
        usr = json.loads(r.get('user_session').encode('utf-8'))
        player_id = usr[str(mass_dec['user_name'])]
        game_room_id = mass_dec['game_room_id']
        if player_id in active_set[str(game_room_id)]['player_bet']:
            del active_set[str(game_room_id)]['player_bet'][player_id]


        # set gameroom record in last_session
        session_log = json.loads(r.get('last_session'))
        if str(mass_dec['game_room_id']) in session_log[player_id]['gamerooms'].values():
            total_amount_dict = json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]['total_amount']
            if player_id in total_amount_dict:
                old_earnings = session_log[player_id]['gamerooms'][str(mass_dec['game_room_id'])]['earnings']
                session_log[player_id]['gamerooms'][str(mass_dec['game_room_id'])] = {
                    'earnings': str(float(old_earnings) + float(total_amount_dict[player_id]))
                }
        r.set('last_session', json.dumps(session_log))


        # update sql
        ab = WriteData()
        user_balance = ab.get_user_data(player_id)[0]['virtual_money']
        total_amount_dict = json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]['total_amount']
        if player_id in total_amount_dict:
            temp_balance = float(total_amount_dict[player_id])
            del active_set[str(game_room_id)]['total_amount'][player_id]
        else:
            temp_balance = 0
        ab.append_player_balance(float(player_id), float(user_balance) + float(temp_balance))

        r.set('active_set', json.dumps(active_set))

        #sitted_clients
        sitted_clients_tmp = json.loads(r.get('sitted_clients'))
        sitted_clients = sitted_clients_tmp[str(mass_dec['game_room_id'])]
        sitted_clients[mass_dec['seat_no']] = '-1'
        sitted_clients_tmp[str(mass_dec['game_room_id'])] = sitted_clients
        r.set('sitted_clients',json.dumps(sitted_clients_tmp))

        # remove player from shuffled active players
        player_seq = obj_help.redis_fetch('shuffled_active_players')
        if str(game_room_id) in player_seq:
            if player_id in player_seq[str(game_room_id)]:
                this_sequence = player_seq[str(game_room_id)]
                this_sequence.remove(player_id)
                player_seq[game_room_id] = this_sequence
        obj_help.redis_store('shuffled_active_players', player_seq)

        # put profile photos for sitted clients
        profile_all_gamerooms = json.loads(r.get('profile'))
        if str(mass_dec['game_room_id']) in profile_all_gamerooms.keys():
            profile_dict = json.loads(r.get('profile'))[str(mass_dec['game_room_id'])]
            del profile_dict[mass_dec['seat_no']]
            profile_all_gamerooms[str(mass_dec['game_room_id'])] = profile_dict
            r.set('profile', json.dumps(profile_all_gamerooms))
        else:
            profile_dict = {}


        total_amount = json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]['total_amount']

        #new sitted_clients to write
        sitted_clients = json.loads(r.get('sitted_clients'))[str(game_room_id)]
        mess3 = {
            'game_key': "10" ,
            'sitted_clients': sitted_clients,
            'profile': profile_dict,
            'total_amount': total_amount,
            # 'player_bet': active_set[str(mass_dec['game_room_id'])]['player_bet']
        }
        for client in clients:
            try:
                client.write_message(json.dumps(mass_dec))
                client.write_message(mess3)
            except Exception as e:
                pass


    def game_action(self, mass_dec, clients):
    #    clients = json.loads('active_set')[str(mass_dec['game_room_id'])]['clients']
        oclients = clients
        clients = clients[str(mass_dec['game_room_id'])].values()
        game_room_id = str(mass_dec['game_room_id'])
        #player_id = json.loads(r.get('user_session').encode('utf-8'))[self.get_secure_cookie('qc_user')]
        usr = json.loads(r.get('user_session').encode('utf-8'))
        player_id = usr[mass_dec['user_name']]
        player_seq1 = obj_help.redis_fetch('shuffled_active_players')[game_room_id]
        usr_ult = {}
        ind1 =0 #next player id
        ind2 =0 #next player index
        ind3 =0 #current player index
        for i,j in usr.iteritems():
            usr_ult[j] = i
        #naming convention
        #iterate the player_seq list and give the next player the turn to play
        sitted_clients = json.loads(r.get('sitted_clients'))[str(mass_dec['game_room_id'])]
        for ind,val in enumerate(player_seq1):
            if val == usr[mass_dec['user_name']]:
                ind2 = (ind +1)%len(player_seq1)
                ind1 = player_seq1[ind2]
                for seat,u_name in sitted_clients.iteritems():
                    if u_name != '-1':
                        if ind1 == usr[u_name]:
                            mass_dec['curr_seat_no'] = seat
                            waiting_for = mass_dec['curr_seat_no']
                            ind3 = ind
        # no action if player is all_in
        opp = json.loads(r.get('active_set'))
        all_in_list = opp[str(mass_dec['game_room_id'])]['all_in_list']
        if player_id not in all_in_list:
            #call the particular function based on user action
            if mass_dec['action'] == 'call':
                obj_help.call(player_id, game_room_id)
            elif mass_dec['action'] == 'check':
                obj_help.check(player_id, game_room_id)
            elif mass_dec['action'] == 'bet':
                obj_help.bet(player_id, game_room_id, mass_dec['bet_amount'])
            elif mass_dec['action'] == 'fold':
                time.sleep(1)
                obj_help.fold(player_id, game_room_id)
                player_seq1 = obj_help.redis_fetch('shuffled_active_players')[game_room_id]
                print player_seq1, 'This is '
                if len(player_seq1) == 1:
                    obj_help.divide_cash_len(game_room_id,player_seq1[0])
                    print "start set called after fold:"
                    self.start_set(mass_dec, oclients)
            elif mass_dec['action'] == 'all_in':
                obj_help.all_in(player_id, game_room_id)
                if player_id not in all_in_list:
                    all_in_list.append(player_id)
                    opp = json.loads(r.get('active_set'))
                    opp[str(mass_dec['game_room_id'])]['all_in_list'] = all_in_list
                    r.set('active_set',json.dumps(opp))


        # updates for front end
        active_set = json.loads(r.get('active_set'))[game_room_id]
        print active_set, 'This is active set'
        mass_dec['pot_amount'] = active_set['pot_amount']
        # print mass_dec['pot_amount'], 'This is Pot Amount'
        # print mass_dec['action'], 'THis is actions'
        mass_dec['user_amount'] = active_set['total_amount'][usr[mass_dec['user_name']]]
        mass_dec['call_amount'] = float(active_set['current_max_bet']) - float(active_set['player_bet'][ind1])
        mass_dec['bet_amount'] = 2*float(active_set['current_max_bet']) - float(active_set['player_bet'][ind1])
        mass_dec['next_user_amount'] = active_set['total_amount'][ind1]
        round_no = active_set['round_no']
        if round_no < 5:
            for client in clients:
                client.write_message(json.dumps(mass_dec))

        #based on the round no. write the required hints to all the clients,
        #this will be true if ind3 == 0, specifying the beginning of next round
        active_set = json.loads(r.get('active_set'))[game_room_id]

        # check if round should continue or not
        round_end = True
        for player in obj_help.redis_fetch('shuffled_active_players')[game_room_id]:
            if active_set['player_bet'][player] == active_set['current_max_bet']:
                continue
            if player in all_in_list:
                continue
            round_end = False

        last_player = r.get('higgest_bidder')

        # finish betting round
        # if ind3 == 2%len(player_seq1) and len(player_seq1) >1 :
        if player_id == last_player and round_end:

            print "i am here again"
            print  round_end 
            req = active_set['req']


            if round_no == 2:
                mass_dec['game_key'] = '6'
                mass_dec['con_id'] = 'cat_' + str(round_no)
                mass_dec['con'] = req['success']['data']['d1'][2]
            elif round_no == 3:
                mass_dec['game_key'] = '6'
                mass_dec['con_id'] = 'cat_' + str(round_no)
                mass_dec['con'] = req['success']['data']['d1'][3]
            elif round_no == 4:
                mass_dec['game_key'] = '6'
                mass_dec['con_id'] = 'question'
                # mass_dec['question_viewers'] = redis_fetch('shuffled_active_players')[game_room_id]
                # print mass_dec['question_viewers'],'<------------'
                mass_dec['con'] = req['success']['data']['question'][0]
                mass_dec['opt'][0] = req['success']['data']['ans'][0]
                mass_dec['opt'][1] = req['success']['data']['ans'][1]
                mass_dec['opt'][2] = req['success']['data']['ans'][2]
                mass_dec['opt'][3] = req['success']['data']['ans'][3]
            elif round_no == 5:
                mass_dec['game_key'] ='6'
                mass_dec['con_id'] = 'round_end'
            round_no += 1
            opp[str(mass_dec['game_room_id'])]['round_no'] = round_no
            r.set('active_set',json.dumps(opp))

            active_player_list = obj_help.redis_fetch('shuffled_active_players')[str(mass_dec['game_room_id'])]
            sb_amount =  obj_help.redis_fetch('active_set')[str(mass_dec['game_room_id'])]['small_blind']
            small_blind = sitted_clients.keys()[sitted_clients.values().index(usr_ult[active_player_list[1%len(active_player_list)]])]
            bb_amount =  obj_help.redis_fetch('active_set')[str(mass_dec['game_room_id'])]['big_blind']
            big_blind = sitted_clients.keys()[sitted_clients.values().index(usr_ult[active_player_list[2 % len(active_player_list)]])]
            mass_dec['small_blind'] = small_blind
            mass_dec['sb_amount'] = sb_amount
            mass_dec['big_blind'] = big_blind
            mass_dec['bb_amount'] = bb_amount
            for client in clients:
                print "abc"
                print mass_dec
                client.write_message(json.dumps(mass_dec))

    def winning_amount(self, mass_dec, right_ans):
        acc = json.loads(r.get('active_set'))
        pot_won = str(math.floor(0.9 * (acc[str(mass_dec['game_room_id'])]['pot_amount']) / len(right_ans.keys())))
        return pot_won

    def submit_ans(self, mass_dec, clients):
        opp = json.loads(r.get('active_set'))
        print('this is opp', opp)
        ans_submit = opp[str(mass_dec['game_room_id'])]['ans_submit']
        ans_submit +=1
        opp[str(mass_dec['game_room_id'])]['ans_submit'] = ans_submit
        r.set('active_set', json.dumps(opp))
        req = opp[str(mass_dec['game_room_id'])]['req']
        oclients=clients
        clients = clients[str(mass_dec['game_room_id'])].values()
        #compare the user's ans with the correct ans, and display the required information
        if int(req['success']['data']['c_ans'][0]) == int(mass_dec['ans']):

            mass_dec['correct_answer'] = req['success']['data']['c_ans'][0]
            mass_dec['game_key'] = '8'
            answer = 1
            game_room_id = str(mass_dec['game_room_id'])
            kk = json.loads(r.get('right_ans').decode('utf-8'))
            right_ans = kk[game_room_id]

            usr = json.loads(r.get('user_session').encode('utf-8'))
            right_ans[usr[mass_dec['user_name']]] = mass_dec['user_name']
            # mass_dec['correct_ans'] =  
            kk[game_room_id] = right_ans
            r.set('right_ans',json.dumps(kk))
            mass_dec['pot_won'] = self.winning_amount(mass_dec, right_ans)

        else:
            mass_dec['game_key'] = '9'
            mass_dec['correct_answer'] = req['success']['data']['c_ans'][0]
            answer = 0

        #post the required stats to the question_statistics api
        usr = json.loads(r.get('user_session').encode('utf-8'))
        player_id = usr[mass_dec['user_name']]
        ans_stat =  {mass_dec['game_room_id'] :{ player_id   : '|'.join([str(answer), mass_dec['answer_time']]) }}
        requests.post('http://localhost:8088/question_statistics', data = {'user_data':json.dumps(ans_stat)})

        game_room_id = str(mass_dec['game_room_id'])
        player_seq = obj_help.redis_fetch('shuffled_active_players')[game_room_id]
        
    #    clients = opp[game_room_id]['clients']
        for client in clients:
                client.write_message(json.dumps(mass_dec))
        
        
        
        #call the divide_cash function once every user has submitted the ans
        if ans_submit == len(player_seq):
            acc = json.loads(r.get('active_set'))
            obj_help.divide_cash(game_room_id)
            
            time.sleep(3)
    
            #send the winners of each round 
            mass_dec['game_key'] = '11'
            kk = json.loads(r.get('right_ans').decode('utf-8'))
            right_ans = kk[game_room_id]
            mass_dec['right_ans_usr']= right_ans.values()
    
            for client in clients:
                client.write_message(json.dumps(mass_dec))
            
            #writing winners and pot amount
            if len(right_ans.keys()) > 0:
                win_mess_lis =""
                for val in right_ans.values():
                    win_mess_lis += val + ", "
                pot_won = str(math.floor(0.9 * (acc[str(mass_dec['game_room_id'])]['pot_amount']) / len(right_ans.keys())))
                rake = str(0.1 * (acc[str(mass_dec['game_room_id'])]['pot_amount']) / len(right_ans.keys()))
                win_mess_1 = json.dumps({
                        'game_key': '1',
                        'user_name': "Winners",
                        'message': str(win_mess_lis)
                })

                win_mess_2 = json.dumps({
                        'game_key': '1',
                        'user_name': "Pot Amount Won",
                        'message': pot_won
                })

                win_mess_3 = json.dumps({
                        'game_key': '1',
                        'user_name': "Rake For The Round",
                        'message': rake
                })


                for client in clients:
                    print "HELLO::: "
                    print win_mess_1,win_mess_2
                    client.write_message(win_mess_1)
                    client.write_message(win_mess_2)
                    client.write_message(win_mess_3)
            else:
                loss_mess_1 = json.dumps({
                        'game_key': '1',
                        'user_name': "Pot Amount",
                        'message': str( (acc[str(mass_dec['game_room_id'])]['pot_amount']) )
                })
                for client in clients:
                    client.write_message(loss_mess_1)
            
            wallet_operation_obj = WriteData()
            # udate wallets after winner is displayed
            total_amount_dict = json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]['total_amount']
            balance = {}
            for player_id in total_amount_dict:
                balance[player_id] = float(wallet_operation_obj.get_user_data(player_id)[0]['virtual_money']) + float(total_amount_dict[player_id])
    
            # send update message on websocket
            msg = {}
            msg['game_key'] = 'update_wallet'
            msg['balance'] = balance
            for client in clients:
                client.write_message(json.dumps(msg))
    
            sitted_clients = json.loads(r.get('sitted_clients'))
            sitted_clients_for_gameroom = sitted_clients[str(mass_dec['game_room_id'])]
            usr_ult = {}
            for i, j in usr.iteritems():
                usr_ult[j] = i
    
            players_for_buyin = []
            players_for_game = []
    
            # check balances
            balance_dict = json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]['total_amount']
            for player in balance_dict:
                if balance_dict[player] <= 0:
                    players_for_buyin.append(player)
                    # username = usr_ult[player]
                    active_set = json.loads(r.get('active_set').decode('utf-8'))
                    total_amount_dict = json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]['total_amount']
                    if player in total_amount_dict:
                        del active_set[str(game_room_id)]['total_amount'][player]
                    r.set('active_set', json.dumps(active_set))
                else:
                    players_for_game.append(player)
    
    
            # send buyin players list on websocket
            message_for_buyin = {
                'game_key': 'buyin_check',
                'player_for_buyin': players_for_buyin,
                'max_buy_in': json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]['max_buy_in'],
                'min_buy_in': json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]['min_buy_in']
            }
            for client in clients:
                client.write_message(json.dumps(message_for_buyin))
    
            time.sleep(3)
    #        idle_gameroom = True
            opp  = json.loads(r.get('active_set'))
            opp[str(mass_dec['game_room_id'])]['idle_gameroom'] = True
            r.set('active_set', json.dumps(opp))
            self.start_set(mass_dec, oclients)
                
    def rebuyin(self, mass_dec, clients):
        oclients = clients
        clients = clients[str(mass_dec['game_room_id'])].values()
        
        # change total amount of player
        active_set = json.loads(r.get('active_set'))
        usr = json.loads(r.get('user_session'))
        player_id = usr[mass_dec['user_name']]
        active_set[str(mass_dec['game_room_id'])]['total_amount'][player_id] = mass_dec['rebuyin']
        r.set('active_set', json.dumps(active_set))
    
        # set gameroom record in last_session
        session_log = json.loads(r.get('last_session'))
        if str(mass_dec['game_room_id']) in session_log[player_id]['gamerooms'].values():
            old_buy_in = session_log[player_id]['gamerooms'][str(mass_dec['game_room_id'])]['buy-in']
            old_earnings = session_log[player_id]['gamerooms'][str(mass_dec['game_room_id'])]['earnings']
            session_log[player_id]['gamerooms'][str(mass_dec['game_room_id'])] = {
                'buy-in': str(float(old_buy_in) + float(mass_dec['rebuyin'])),
                'earnings': str(float(old_earnings) - float(mass_dec['rebuyin']))
            }
        r.set('last_session', json.dumps(session_log))
    
        wallet_operation_obj = WriteData()
        # deduct buy-ins
        user_balance = wallet_operation_obj.get_user_data(player_id)[0]['virtual_money']
        wallet_operation_obj.append_player_balance(float(player_id), float(user_balance) - mass_dec['rebuyin'])
    
        total_amount_dict = json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]['total_amount']
        balance = {}
        balance[player_id] = float(wallet_operation_obj.get_user_data(player_id)[0]['virtual_money']) + float(total_amount_dict[player_id])
    
        # send update message on websocket
        msg = {}
        msg['game_key'] = 'update_wallet'
        msg['balance'] = balance
        for client in clients:
            client.write_message(json.dumps(msg))
    
        idle_gameroom = json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]['idle_gameroom']
        if len(json.loads(r.get('active_set'))[str(mass_dec['game_room_id'])]['total_amount']) > 1 and idle_gameroom:
            # start the game
            automated_start = {
                'user_name': 'admin',
                'game_room_id': str(mass_dec['game_room_id'])
            }
            self.start_set(json.dumps(automated_start), oclients)
    
    
                # # resume on seat
        # sitted_clients = json.loads(r.get('sitted_clients'))
        # sitted_clients_for_gameroom = sitted_clients[str(mass_dec['game_room_id'])]
        # sitted_clients_for_gameroom[mass_dec['seat_no']] = mass_dec['user_name']
        # sitted_clients[str(mass_dec['game_room_id'])] = sitted_clients_for_gameroom
        # r.set('sitted_clients', json.dumps(sitted_clients))
        
        
    def sit_here_func(self, mass_dec, clients):
        #client_gameplay.append(self)
        clients = clients[str(mass_dec['game_room_id'])].values()        
        #when a players sits, information is updated in redis active_set table, balance is fetched from sql and player_bet is initialised to 0
        active_set = json.loads(r.get('active_set').decode('utf-8'))
        usr = json.loads(r.get('user_session').encode('utf-8'))
        player_id = usr[str(mass_dec['user_name'])]
        active_set[str(mass_dec['game_room_id'])]['player_bet'][player_id] = 0
        # balance = self.get_user_data(player_id)[0]['virtual_money']
        # active_set[str(mass_dec['game_room_id'])]['total_amount'][player_id] = balance
        r.set('active_set', json.dumps(active_set))              
    
        #enter the users information in the sitted clients table, and set in the redis table
        sitted_clients_tmp = json.loads(r.get('sitted_clients').decode('utf-8'))
        sitted_clients = {}
        sitted_clients = sitted_clients_tmp[mass_dec['game_room_id']]
        sitted_clients[mass_dec['seat_no']] = mass_dec['user_name']   
        sitted_clients_tmp[str(mass_dec['game_room_id'])] = sitted_clients
        r.set('sitted_clients',json.dumps(sitted_clients_tmp))
    
        # update profile photo for seat
        profile_dict = json.loads(r.get('profile'))
        if str(mass_dec['game_room_id']) in profile_dict.keys():
            profile_dict[str(mass_dec['game_room_id'])][mass_dec['seat_no']] = mass_dec['profile']
        else:
            profile_dict[str(mass_dec['game_room_id'])] = {mass_dec['seat_no']: mass_dec['profile']}
        r.set('profile', json.dumps(profile_dict))
    
        # sz = str(len(client_gameplay))
        # mess2 = { 'game_key': "1" ,'user_name': "Active Clients :", 'message': sz, 'seat_no':"nil", 'action':"nil", 'dealer_seat':'nil' }
        for client in clients:
            client.write_message(json.dumps(mass_dec))
            # client.write_message(mess2)