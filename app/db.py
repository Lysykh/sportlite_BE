#здесь мы будем подключаться к базе данных и потом забрать конкретную сессию

import sqlite3

def get_session(session_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sessions WHERE id = ?', (session_id,))
    session = cursor.fetchone()
    conn.close()
    return session