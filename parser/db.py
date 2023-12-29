import hashlib
import logging
import os
import sqlite3


def init_db():
    db_file = "aura.db"
    if not os.path.exists(db_file):
        with open(db_file, 'w'): pass

    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        # create a new table if nothing exists
        c.execute(
            "CREATE TABLE IF NOT EXISTS assistants (id INTEGER PRIMARY KEY, user_id TEXT, assistant_id TEXT, "
            "thread_id TEXT)")

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
    except Exception as e:
        logging.info("Error occurred while init_db: ", str(e))


def create_assistant_id(user_id, assistant_id, thread_id, db_file):
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        # Update the existing row
        c.execute("UPDATE assistants SET assistant_id = ?, thread_id = ? WHERE user_id = ?",
                  (assistant_id, thread_id, user_id))

        conn.commit()
        conn.close()
    except Exception as e:
        logging.info("Error occurred while create_user: ", str(e))
