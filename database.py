# users_db.py

import os
import sqlite3

class UsersDB:
    def __init__(self, db_name='users_database.db'):
        self.db_name = db_name

        # Создаем папку для базы данных, если ее нет
        os.makedirs(os.path.dirname(os.path.abspath(db_name)), exist_ok=True)

        # Подключаемся к базе данных (если ее нет, она будет создана)
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                middle_name TEXT,
                phone_number TEXT,
                username TEXT,
                telegram_id INTEGER,
                birth_date TEXT,
                description TEXT,
                interests TEXT
            )
        ''')

        self.conn.commit()

    def add_user(self, first_name, last_name, middle_name, phone_number, username, telegram_id, birth_date, description=None, interests=None):
        self.cursor.execute('''
            INSERT INTO users (first_name, last_name, middle_name, phone_number, username, telegram_id, birth_date, description, interests)
            # VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, middle_name, phone_number, username, telegram_id, birth_date, description, interests))

        self.conn.commit()

    def get_all_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()
