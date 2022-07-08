import sqlite3
import config

conn = sqlite3.connect(config.db_file, check_same_thread=False)
cursor = conn.cursor()


def add_new_user(user_id, user_name, states):
    cursor.execute('INSERT INTO user_status(user_id, user_name, States) VALUES(?,?,?)', (user_id, user_name, states))
    conn.commit()


def table_value(user_id):
    try:
        cursor.execute("SELECT * FROM user_status;")
        all_results = cursor.fetchall()
        for date in all_results:
            if date[0] == user_id:
                return True
    except PermissionError:
        return False
    finally:
        conn.commit()


def get_state(user_id):
    cursor.execute("SELECT * FROM user_status;")
    all_results = cursor.fetchall()
    for date in all_results:
        if date[0] == user_id:
            values = date[2]
        conn.commit()
    return values


def set_state(user_id, value):
    cursor.execute("UPDATE user_status SET States =" + str(value) + " WHERE user_id = " + str(user_id))
    conn.commit()