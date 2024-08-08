import sqlite3
from datetime import datetime
def get_connection():
    return sqlite3.connect("message.db")

# make the sqlite datebase tables

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            creation_time TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message_text TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()




# Function to check if a user exists
def user_exists(user_id:int) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM users WHERE id = ?', (user_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

# Function to add a new user
def add_user(user_id:int) -> None:
    if not user_exists(user_id):
        creation_time = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (id , creation_time)
            VALUES (?, ?)
        ''', (user_id, creation_time))
        conn.commit()
        conn.close()

# Function to add a new message
def add_message(user_id:int, message_text:str) -> None:
    if user_exists(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (user_id, message_text)
            VALUES (?, ?)
        ''', (user_id, message_text))
        conn.commit()
        conn.close()
    else:
        print("User ID does not exist. Please add the user first.")


def get_last_15_messages(user_id:int) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT message_text FROM messages
        WHERE user_id = ?
        ORDER BY ROWID DESC
        LIMIT 20
    ''', (user_id,))
    messages = cursor.fetchall()
    conn.close()
    return [message[0] for message in messages][::-1]  # Reverse to get in chronological order



if __name__ == "__main__":
    create_tables()
    user_exists()
    get_last_15_messages()
    get_connection()
    add_message()
