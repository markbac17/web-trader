import sqlite3
import os

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, 'trader.db')

def seed(dbpath=DBPATH):
    with sqlite3.connect(dbpath) as conn:
        cur = conn.cursor()

        sql = """
                INSERT INTO accounts (
                username, password_hash, balance, api_key
                ) VALUES ('test_user', 'some_password_hash', 1, '1234567890123456789');
              """
        cur.execute(sql)

if __name__ == "__main__":
    seed()