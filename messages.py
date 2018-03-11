class errors():
    def __init__(self):
        self.error_code_unauthorized = 401
        self.error_code_not_found = 404
        self.error_code_resource_exists = 405
        self.error_code_forbidden = 403
        self.error_message_empty_field = "Email or password is empty"
        self.error_message_email_id_exists = "Email_id already exists"
        self.error_message_username_exists = "User_name already exists"
        self.error_message_empty_field = "Email or password is empty"
        self.error_message_unauthorized_user = "User Not found or either deleted"
        self.error_message_unauthorized_password = "Incorrect Passowrd"
        self.error_no_active_games = "No active games currently"
        self.error_message_login = "PLEASE LOGIN"


class success():
    def __init__(self):
        self.success_code_Ok = 200
        self.success_code_created = 201
        self.success_message_user = "Login Successfull."
        self.success_message_user_create = "User created successfully"



