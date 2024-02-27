from flask_login import current_user

class UsersPolicy:
    def __init__(self, record):
        self.record = record

    def delete_item(self):
        return current_user.is_admin()

    def create_item(self):
        return current_user.is_admin()

    def edit_item(self):
        return current_user.is_admin() or current_user.is_moder()
    
