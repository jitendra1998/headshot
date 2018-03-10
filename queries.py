
class SQLqueries():
    def __init__(self):
        self.check_username = self.check_username = "SELECT * FROM user WHERE user_name = '%s' AND deleted_at IS NULL"

        self.check_email = "SELECT * FROM user WHERE email ='%s' AND deleted_at IS NULL"

        # self.create_user = "INSERT INTO user (user_name,email,password,first_name,last_name," \
        #                    "virtual_money,date_of_birth,gender,country,created_at) VALUES" \
        #                    " ('%s','%s','%s','%s','%s',%d,'%s','%s','%s','%s')"

        self.create_user = "INSERT INTO user (user_name,email,password,first_name,last_name," \
                           "virtual_money,date_of_birth,gender,country,created_at,profile_image) VALUES" \
                           " ('%s','%s','%s','%s','%s',%d,'%s','%s','%s','%s','%s')"

        self.login_email_check = "SELECT * FROM user" \
                                 " WHERE email = '%s' AND deleted_at IS NULL"

        self.login_pass_check = "Select * FROM user " \
                                "WHERE email = '%s' AND password = '%s' AND deleted_at IS NULL"

        self.show_active_games = "select id AS game_room_id, game_room_name, game_category, max_players, game_theme, min_buy_in, max_buy_in, big_blind, small_blind from game_room where id = %d"
        
        # self.show_user_data = "SELECT id, user_name, virtual_money from user where id = %d"
        self.show_user_data = "SELECT id, user_name, virtual_money, profile_image from user where id = %d"
