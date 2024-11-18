import mysql.connector
from datetime import datetime
from mysql.connector import Error

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="reminders"
            )
            self.cur = self.conn.cursor()
            print("Database connection established.")
        except Error as e:
            print(f"Error connecting to database: {e}")
            self.conn = None

    ##### Add_user #####
    def add_user(self, id):
        if not self.conn:
            print("No database connection.")
            return False

        try:
            self.cur.execute("SELECT user_id FROM users WHERE user_id=%s", (str(id),))
            result = self.cur.fetchone()
            if not result:
                self.cur.execute("INSERT INTO users VALUES (%s, %s, %s)", (str(id), '0', "None"))
                self.conn.commit()
                print(f"User {id} added successfully.")
                return True
            else:
                print(f"User {id} already exists.")
        except Error as e:
            print(f"Database error in add_user: {e}")
        return False

    ##### Update_user #####
    def update_user(self, id, client):
        try:
            # بررسی وجود کاربر با user_id
            self.cur.execute("SELECT client FROM users WHERE user_id = %s", (client,))
            result = self.cur.fetchone()

            if result:  # اگر کاربر وجود دارد
                current_client = result[0]
                if not current_client or current_client == '0':  # اگر client خالی یا پیش‌فرض باشد
                    self.cur.execute(
                        "UPDATE users SET client = %s WHERE user_id = %s",
                        (id, client)
                    )
                    self.conn.commit()
                    print(f"User {client} updated with referrer {id}.")
                    return True
                else:
                    print(f"User {client} already has a referrer: {current_client}.")
            else:
                print(f"User {client} does not exist in the database.")

        except Exception as e:
            print(f"Error in update_user: {e}")

        return False


    ##### All_user #####
    def all_user(self):
        if not self.conn:
            print("No database connection.")
            return []

        try:
            self.cur.execute("SELECT user_id FROM users")
            users = [j[0] for j in self.cur.fetchall()]
            return users
        except Exception as e:
            print(f"Error retrieving all users: {e}")
            return []

    ##### Check_block #####
    def check_block(self, id):
        if not self.conn:
            print("No database connection.")
            return True

        try:
            self.cur.execute("SELECT stat FROM users WHERE user_id=%s", (str(id),))
            result = self.cur.fetchone()
            if result and result[0] == "None":
                return False
            return True
        except Exception as e:
            print(f"Error checking block: {e}")
            return True

    ##### Add_block #####
    def add_block(self, id):
        if not self.conn:
            print("No database connection.")
            return False

        try:
            self.cur.execute("SELECT stat FROM users WHERE user_id=%s", (str(id),))
            result = self.cur.fetchone()
            if result and result[0] == "None":
                self.cur.execute("UPDATE users SET stat=%s WHERE user_id=%s", ("block", str(id)))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Error adding block: {e}")
        return False

    ##### Remove_block #####
    def remove_block(self, id):
        if not self.conn:
            print("No database connection.")
            return False

        try:
            self.cur.execute("SELECT stat FROM users WHERE user_id=%s", (str(id),))
            result = self.cur.fetchone()
            if result and result[0] == "block":
                self.cur.execute("UPDATE users SET stat=%s WHERE user_id=%s", ("None", str(id)))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Error removing block: {e}")
        return False

    ##### Add_reminder #####
    def add_reminder(self, chat_id, reminder, remind_time):
        if not self.conn:
            print("No database connection.")
            return False

        try:
            self.cur.execute("INSERT INTO reminders (chat_id, reminder, remind_time) VALUES (%s, %s, %s)",
                             (chat_id, reminder, remind_time))
            self.conn.commit()
            print(f"Reminder added for chat_id {chat_id}.")
            return True
        except Exception as e:
            print(f"Error adding reminder: {e}")
        return False

    ##### Get_reminders #####
    def get_reminders(self, chat_id):
        if not self.conn:
            print("No database connection.")
            return []

        try:
            self.cur.execute("SELECT id, reminder, remind_time FROM reminders WHERE chat_id = %s", (chat_id,))
            reminders = self.cur.fetchall()
            return reminders
        except Exception as e:
            print(f"Error retrieving reminders: {e}")
            return []

    ##### Delete_reminder #####
    def delete_reminder(self, id):
        if not self.conn:
            print("No database connection.")
            return False

        try:
            self.cur.execute("DELETE FROM reminders WHERE id = %s", (id,))
            self.conn.commit()
            print(f"Reminder with id {id} deleted.")
            return True
        except Exception as e:
            print(f"Error deleting reminder: {e}")
        return False

    ##### Get_due_reminders #####
    def get_due_reminders(self):
        if not self.conn:
            print("No database connection.")
            return []

        try:
            now = datetime.now()
            self.cur.execute("SELECT id, chat_id, reminder, remind_time FROM reminders WHERE remind_time <= %s", (now,))
            reminders = self.cur.fetchall()
            return reminders
        except Exception as e:
            print(f"Error getting due reminders: {e}")
            return []

    ##### Close #####
    def close(self):
        if not self.conn:
            print("No database connection.")
            return False

        try:
            self.cur.close()
            self.conn.close()
            print("Database connection closed.")
            return True
        except Exception as e:
            print(f"Error closing database connection: {e}")
        return False
