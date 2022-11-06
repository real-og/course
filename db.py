import psycopg2
import os
from psycopg2.extras import DictCursor

class Database(object):
    def __init__(self):
        self.conn = psycopg2.connect(
            database=str(os.environ.get('database')),
            user=str(os.environ.get('user')),
            password=str(os.environ.get('password')),
            host=str(os.environ.get('host')),
            port=str(os.environ.get('port'))
        )
        self.curs = self.conn.cursor(cursor_factory=DictCursor)

    def __enter__(self):
        return self.curs

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

def add_user(name, email, password, age):
    with Database() as curs:
        _SQL = f"""INSERT INTO users (name, email, password, age)
                   VALUES ('{name}', '{email}', '{password}', {age});"""
        curs.execute(_SQL)

def get_user_by_email(email):
    with Database() as curs:
        _SQL = f"""SELECT * FROM users WHERE email = '{email}' LIMIT 1;"""
        curs.execute(_SQL)
        return curs.fetchone()

        
