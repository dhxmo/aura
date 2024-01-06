import hashlib
import json
import logging
import os
import sqlite3

from core.config import Config


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

        # create a new table for cookies
        c.execute(
            "CREATE TABLE IF NOT EXISTS cookies (id INTEGER PRIMARY KEY, user_id TEXT, domain TEXT, value TEXT,"
            "FOREIGN KEY (user_id) REFERENCES assistants(user_id))"
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

def add_cookies_to_db(cookie, domain, user_id):
    print("add_cookies_to_db", cookie)

    try:
        conn = sqlite3.connect(Config.db_file) # Connect to the SQLite database
        c = conn.cursor() # Create a cursor object

        # Escape the cookie variable
        escaped_cookie_name = sqlite3.Binary(cookie.encode())

        # Insert cookies into the table
        c.execute("INSERT INTO cookies (user_id, domain, value) VALUES (?, ?, ?)",
                (user_id, domain, escaped_cookie_name))

        # Save (commit) the changes
        conn.commit()

        # Close the connection
        conn.close()
    except Exception as e:
        print("Error occurred while add_cookies_to_db: ", str(e))


def check_cookie_exists(user_id, url, cookie):
   """Check if the cookie already exists in the database. Returns True if cookie exists"""

   conn = sqlite3.connect(Config.db_file)
   c = conn.cursor()

   escaped_cookie_name = sqlite3.Binary(cookie.encode())

   c.execute("SELECT * FROM cookies WHERE user_id = ? AND domain = ? AND value = ?",
             (user_id, url, escaped_cookie_name))
   existing_cookie = c.fetchone()
   conn.close()

   return existing_cookie is not None


def load_cookies(user_id):
    # load cookies. refresh every 30 days

    conn = sqlite3.connect(Config.db_file) # Connect to the SQLite database
    c = conn.cursor() # Create a cursor object

    # Load cookies from the database
    c.execute("SELECT * FROM cookies WHERE user_id = ?", (user_id,))
    rows = c.fetchall()

    return rows
   # for row in rows:
   #     driver.add_cookie({
   #         'name': row[1],
   #         'value': row[2],
   #         'domain': row[3],
   #         'path': row[4],
   #         'expiry': row[5],
   #         'httpOnly': row[6],
   #         'secure': row[7]
   #     })

