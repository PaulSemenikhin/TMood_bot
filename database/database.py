import sqlite3

conn = sqlite3.connect('data.db')
cur = conn.cursor()
# SQL-запрос на создание таблицы "users"
cur.execute('CREATE TABLE IF NOT EXISTS users ('
            'user_id INTEGER UNIQUE, '
            'date_start_bot DATE, '
            'time_notify TIME, '
            'depression_notification INTEGER DEFAULT 0, '
            'depression_time DATE, '
            )

# SQL-запрос на создание таблицы "moods"
cur.execute('CREATE TABLE IF NOT EXISTS moods ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'user_id INTEGER, '
            'date DATETIME, '
            'mood_value INTEGER, '
            'other_field TEXT, '
            'FOREIGN KEY (user_id) REFERENCES users (user_id) ON '
            'DELETE CASCADE)')
# TODO: протестировать как он каскадно удаляет записи.
