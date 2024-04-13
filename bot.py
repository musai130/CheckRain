import sqlite3
from config import ADMIN_ID
import time
class BotBD:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute(
            "SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, user_id):

        self.cursor.execute(
            "INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def get_users(self):
        return self.cursor.execute("SELECT `user_id` FROM `users`").fetchall()
    
    def set_time_sub(self, time_sub, user_id):
        self.cursor.execute("UPDATE `users` SET `time_sub` = ? WHERE `user_id` = ? ", (time_sub, user_id,))
        return self.conn.commit()
    
    def get_time_sub(self, user_id):
        result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `user_id` = ? ", (user_id,)).fetchall()
        for row in result:
            time_sub = int(row[0])
        return time_sub
    def get_sub_status(self, user_id):
        result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `user_id` = ? ", (user_id,))
        for row in result:
            time_sub = int(row[0])
        if time_sub > int(time.time()):
            return True
        else:
            return False
        
    def check_admin(self, user_id):
        for i in range(len(ADMIN_ID)):
                if user_id == ADMIN_ID[i]:
                    return True
        return False

