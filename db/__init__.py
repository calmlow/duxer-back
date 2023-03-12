import sqlite3
import logging
import logging.config
from calmlogging import get_logger
from pathlib import Path

log = get_logger(__file__)

DATABASE_FILE = './resources/database.db'
SCHEMA_FILE = './resources/schema.sql'

#connection = sqlite3.connect(DATABASE_FILE)
#connection = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
# db_conn = sqlite3.connect(DATABASE_FILE)
#db_conn = None


def select(query, params=None):
    log.info("Query: {}", query)
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        log.info("Executing query: %s" % query)
        if params:
            result = cur.execute(query, params).fetchall()
        else:
            result = cur.execute(query).fetchall()
        return result
    except sqlite3.Error as e:
        log.error("Error while connecting to sqlite. {}", e)
        log.error("I will try to create the database file.")
        # try setting up the database
        # setup_db()
        # return select(query)


def upsert(query, params=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()


def get_db_connection():
    #global db_conn
    # if db_conn is not None:
    #    return db_conn

    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row
        db_conn = conn
        return conn
    except sqlite3.Error as e:
        print(e)
        log.error("Error while connecting to sqlite.")
        print("Error while connecting to sqlite.")
        print("I will try to create the database file.")
        # try setting up the database

        Path(DATABASE_FILE).touch()
        setup_db()


def setup_db():
    conn = get_db_connection()
    with open(SCHEMA_FILE) as f:
        conn.executescript(f.read())

    cur = conn.cursor()

    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                ('First Post', 'Content for the first post')
                )

    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                ('Second Post', 'Content for the second post')
                )

    conn.commit()
    # conn.close()
