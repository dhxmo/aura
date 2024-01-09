import hashlib
import os
import sqlite3

from aura.core.config import Config


def init_db(db_file):
    if not os.path.exists(db_file):
        with open(db_file, 'w'): pass

    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        c.execute(
            "CREATE TABLE IF NOT EXISTS assistants (id INTEGER PRIMARY KEY, user_id TEXT, assistant_id TEXT, "
            "thread_id TEXT)"
        )

        # select user row
        c.execute("SELECT * FROM assistants LIMIT 1")
        user = c.fetchone()

        # if user doesnt exist, add a new user
        if not user:
            user_id = hashlib.sha256(str(id).encode()).hexdigest()

            # Remove the id from the INSERT statement since it's now auto-generated
            c.execute("INSERT INTO assistants (user_id) VALUES (?)", (user_id,))

            conn.commit()
            conn.close()
        else:
            user_id = user[1]

        return user_id
    except Exception as e:
        print("Error occurred while init_db: ", str(e))


def create_assistant_id(user_id, assistant_id, thread_id):
    try:
        conn = sqlite3.connect(Config.db_file)
        c = conn.cursor()

        # Update the existing row
        c.execute("UPDATE assistants SET assistant_id = ?, thread_id = ? WHERE user_id = ?",
                  (assistant_id, thread_id, user_id))

        conn.commit()
        conn.close()
    except Exception as e:
        print("Error occurred while create_user: ", str(e))
