import sqlite3


DATABASE_NAME = 'users.db'


def init_db():
    with connect:
        cursor = connect.cursor()
        # Создание таблицы, если она не существует
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL UNIQUE
            )
        ''')


def create_user(user_id):
    with connect:
        cursor = connect.cursor()
        try:
            cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
            print(f"User with user_id {user_id} created.")
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}. User with user_id {user_id} already exists.")


def get_all_user_ids():
    with connect:
        cursor = connect.cursor()
        cursor.execute('SELECT user_id FROM users')
        user_ids = cursor.fetchall()
        return [user_id[0] for user_id in user_ids]


connect = sqlite3.connect(DATABASE_NAME)
init_db()
