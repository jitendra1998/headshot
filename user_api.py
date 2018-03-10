from routes import *
from datetime import datetime
from mysql_configure import MYSQLConfiguration
from common import CommonBaseHandler
from queries import SQLqueries
from messages import errors
from messages import success
import redis
import json
from game_room_api import host
from password_config import PassWords

print host
r = redis.StrictRedis(host='localhost', db=4)

query_obj = SQLqueries()
error_obj = errors()
success_obj = success()
pass_obj = PassWords()

# check validity of email and other parameters
class UserSignup(CommonBaseHandler):
    def check_username(self, user_name):
        cursor_u = self.db.cursor()
        user_sql = query_obj.check_username % user_name
        username_check = cursor_u.execute(user_sql)
        cursor_u.close()
        return username_check

    def check_email(self, email_id):
        cursor_e = self.db.cursor()
        chk_email = query_obj.check_email % email_id
        e = cursor_e.execute(chk_email)
        cursor_e.close()
        return e

    def get(self):
        self.render("sign_up.html")

    def post(self):
        signup_successful = False
        self.set_headers()
        response_data = ""
        user_name = self.get_argument("user_name")
        email = self.get_argument("user_email")
        password = self.get_argument("password")
        firstname = self.get_argument("first_name", default="NULL", strip=False)
        lastname = self.get_argument("last_name", default="NULL", strip=False)
        # v_money = self.get_argument("virtual_money", default=100, strip=False)
        dob = self.get_argument("d_o_b", default="NULL", strip=False)
        gender = self.get_argument("gender", default="NULL", strip=False)
        country = self.get_argument("country", default="NULL", strip=False)

        # get value of profile-image
        profile_photo = self.get_argument("profile-image", default="profile-default.png", strip=False)

        chk_user_name = self.check_username(user_name)

        if chk_user_name != 1:
            if not self.check_email(email):
                signup_successful = True
                cursor = self.db.cursor()
                # create_user_sql = query_obj.create_user % (user_name, email, password, firstname, lastname, 100, dob, gender, country, datetime.now())
                create_user_sql = query_obj.create_user % (
                user_name, email, password, firstname, lastname, 10000, dob, gender, country, datetime.now(),
                profile_photo)
                cursor.execute(create_user_sql)
                self.db.commit()
                user_id = cursor.lastrowid
                cursor.close()

                self.set_secure_cookie("qc_user", str(email))

#                r.set("user_session", user_name, user_id)

                response_data = json.dumps({
                    'success': {
                        'code': success_obj.success_code_created,
                        'message': success_obj.success_message_user_create,
                        'data': {"user_id": user_id}
                    }
                })

            else:
                response_data = json.dumps({
                    'error': {
                        'code': error_obj.error_code_resource_exists,
                        'message': error_obj.error_message_email_id_exists
                    }
                })
        else:
            response_data = json.dumps({
                'error': {
                    'code': error_obj.error_code_resource_exists,
                    'message': error_obj.error_message_username_exists
                }
            })

        # self.write(response_data)
        # self.finish()
        if signup_successful:
            self.redirect('/user/login')
        else:
            self.write(response_data)


class UserLogin(CommonBaseHandler):
    def get(self):
        if not self.get_secure_cookie("auth_cookie"):
            self.redirect('/authenticate/user')
        else:
            # self.write("Your cookie was set!")
            self.render("login.html")

        # self.render("login.html")

    def post(self):
        self.set_headers()
        response_data = ""
        email = self.get_argument("user_email")
        password = self.get_argument("password")
        if email and password:
            # hit the sql once
            cursor = self.db.cursor()
            email_sql = query_obj.login_email_check % email
            user = cursor.execute(email_sql)
            password_sql = query_obj.login_pass_check % (email, password)
            check_pass = cursor.execute(password_sql)
            return_dict = {}
            if r.get('user_session'):
                return_dict = json.loads(r.get('user_session').decode('utf-8'))
            if user:
                if check_pass:
                    user_data = cursor.fetchall()
                    if user_data[0][1] not in return_dict:
                        return_dict[str(user_data[0][1])] = str(user_data[0][0])
                        # user_id = []
                    # user_name = ""
                    # for row in user_data:
                    #     user_id.append(row[0])
                    #     user_name = row[1]
                    print user_data[0][1], 'This is qc_user'
                    self.set_secure_cookie("qc_user", user_data[0][1])
                    # d = {}
                    # d = {user_name: user_id}
                    print return_dict, 'This is return dict'
                    r.set("user_session", json.dumps(return_dict))
                    # after check pass

                    # create user's entry in last session on login
                    # session history = { user_id : { start_time, duration, gamerooms : [ gameroom_id : {buy-in, earning}], net_earnings}}
                    if not r.get('last_session'):
                        session_log = {}
                    else:
                        session_log = json.loads(r.get('last_session'))
                    # update start_time on login
                    session_log[str(user_data[0][0])] = {'start_time': str(datetime.now()),
                                                         'duration': None,
                                                         'gamerooms': {},
                                                         'end_time' : None,
                                                         'net_earnings': None
                                                         }
                    r.set("last_session", json.dumps(session_log))
                    self.redirect('/user/view_games')

                    response_data = json.dumps({
                        'success': {
                            'code': success_obj.success_code_Ok,
                            'message': success_obj.success_message_user,
                            'data': {"user_id": user_data[0][0]}
                        }
                    })
                else:
                    response_data = json.dumps({
                        'error': {
                            'code': error_obj.error_code_unauthorized,
                            'message': error_obj.error_message_unauthorized_password
                        }
                    })
                    self.write(response_data)
            else:
                # self.redirect('/user/login')
                response_data = json.dumps({
                    'error': {
                        'code': error_obj.error_code_unauthorized,
                        'message': error_obj.error_message_unauthorized_user
                    }
                })
                self.write(response_data)
        else:
            # self.redirect('/user/login')
            response_data = json.dumps({
                'error': {
                    'code': error_obj.error_code_unauthorized,
                    'message': error_obj.error_message_empty_field
                }
            })
            self.write(response_data)


class UserLogout(CommonBaseHandler):
    def post(self):
#        user_session = json.loads(r.get('user_session'))
#        user_id = user_session[self.get_secure_cookie("qc_user")]

        # save activity of last session
#        session_log = json.loads(r.get('last_session'))

        # save duration
#        start_time = str(session_log[user_id]['start_time'])
#        end_time = str(datetime.now())
#        session_log[user_id]['end_time'] = end_time
#        start = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
#        end = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
#        session_log[user_id]['duration'] = str(end - start)


#        net_earnings = 0
        # calculate total earnings in this session
#        if session_log[user_id]['gamerooms']:
#            for gameroom in session_log[user_id]['gamerooms']:
#                net_earnings = int(net_earnings) + int(session_log[user_id]['gamerooms'][gameroom]['earnings'])
#        session_log[user_id]['net_earnings'] = str(net_earnings)

        # delete player from user_session
#        del user_session[self.get_secure_cookie("qc_user")]

        # clear cookie
#        self.clear_cookie("qc_user")

#        r.set('last_session', json.dumps(session_log))
#        r.set('user_session', json.dumps(user_session))
#        self.redirect('/user/login')
        print "LOGOUT CALLED:  "


class AdminLogin(CommonBaseHandler):
    def get(self):
        if not self.get_secure_cookie("auth_cookie"):
            self.redirect('/authenticate/admin')
        else:
            self.render("admin_log.html")

    def post(self):
        self.set_headers()
        response_data = ""
        email = self.get_argument("user_email")
        password = self.get_argument("password")

        if email =='admin@admin.com' and password == 'admin':
            # hit the sql once
            cursor = self.db.cursor()
            email_sql = query_obj.login_email_check % email
            user = cursor.execute(email_sql)
            password_sql = query_obj.login_pass_check % (email, password)
            check_pass = cursor.execute(password_sql)
            return_dict = {}
            if r.get('user_session'):
                return_dict = json.loads(r.get('user_session').decode('utf-8'))
            if user:
                if check_pass:
                    user_data = cursor.fetchall()
                    if user_data[0][1] not in return_dict:
                        return_dict[str(user_data[0][1])] = str(user_data[0][0])
                    self.set_secure_cookie("qc_user", user_data[0][1])
                    r.set("user_session", json.dumps(return_dict))
                    if not r.get('last_session'):
                        session_log = {}
                    else:
                        session_log = json.loads(r.get('last_session'))
                    session_log[str(user_data[0][0])] = {'start_time': str(datetime.now()),
                                                         'duration': None,
                                                         'gamerooms': {},
                                                         'end_time' : None,
                                                         'net_earnings': None
                                                         }
                    r.set("last_session", json.dumps(session_log))
                    self.redirect("http://52.163.123.180:8081/admin_panel.html")

                    response_data = json.dumps({
                        'success': {
                            'code': success_obj.success_code_Ok,
                            'message': success_obj.success_message_user,
                            'data': {"user_id": user_data[0][0]}
                        }
                    })
                else:
                    response_data = json.dumps({
                        'error': {
                            'code': error_obj.error_code_unauthorized,
                            'message': error_obj.error_message_unauthorized_password
                        }
                    })
                    self.write(response_data)
            else:
                response_data = json.dumps({
                    'error': {
                        'code': error_obj.error_code_unauthorized,
                        'message': error_obj.error_message_unauthorized_user
                    }
                })
                self.write(response_data)
        else:
            response_data = json.dumps({
                'error': {
                    'code': error_obj.error_code_unauthorized,
                    'message': error_obj.error_message_empty_field
                }
            })
            self.write(response_data)



class WebSite(CommonBaseHandler):
    def get(self):
        self.render("index_without_youtube.html")


class PrivateAccessAutheticate(tornado.web.RequestHandler):
    def get(self):
        self.redirect('')

    def post(self):
        u = self.get_body_argument("u")
        p = self.get_body_argument("p")

        if u in pass_obj.dic:
            if pass_obj.dic[u] == p:
                print '< -------------- User Login ----------------------->'
                self.set_secure_cookie("auth_cookie", u, expires_days=1)
                self.redirect('/user/login')
            else:
                self.redirect('')
        else:
            self.redirect('')



class PrivateAccessAutheticateAdmin(tornado.web.RequestHandler):
    def get(self):
        self.redirect('')

    def post(self):
        u = self.get_body_argument("u")
        p = self.get_body_argument("p")

        if u in pass_obj.dic:
            if pass_obj.dic[u] == p:
                print '< -------------- Admin Login ----------------------->'
                self.set_secure_cookie("auth_cookie", u, expires_days=1)
                self.redirect('/admin')
            else:
                self.redirect('')
        else:
            self.redirect('')


