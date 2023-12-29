import hashlib
import logging
import sqlite3


def create_user(db_file):
    user_id = hashlib.sha256(str(id).encode()).hexdigest()
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        # Modify the CREATE TABLE statement to use INTEGER PRIMARY KEY
        c.execute("CREATE TABLE IF NOT EXISTS assistants (id INTEGER PRIMARY KEY, user_id TEXT, assistant_id TEXT, "
                  "thread_id TEXT)")

        # Remove the id from the INSERT statement since it's now auto-generated
        c.execute("INSERT INTO assistants (user_id) VALUES (?)", (user_id,))

        conn.commit()
        conn.close()

        return True
    except Exception as e:
        logging.info("Error occurred while create_user: ", str(e))


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
