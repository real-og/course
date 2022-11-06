import sqlite3
import time
import math
import re
from flask import url_for
import psycopg2
import os

class Database(object):
    def __init__(self):
        self.conn = psycopg2.connect(
            database=str(os.environ.get('database')),
            user=str(os.environ.get('user')),
            password=str(os.environ.get('password')),
            host=str(os.environ.get('host')),
            port=str(os.environ.get('port'))
        )
        self.curs = self.conn.cursor()

    def __enter__(self):
        return self.curs

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

def getPassHashByEmail(email):
    with Database() as curs:
        _SQL = f"""SELECT password FROM users WHERE email = '{email}';"""
        curs.execute(_SQL)
        res = curs.fetchall()
        if len(res) > 0:
            return res[0][0]
        return None

def addUser(name, email, password, age):
    with Database() as curs:
        _SQL = f"""INSERT INTO users (name, email, password, age)
                   VALUES ('{name}', '{email}', '{password}', {age})"""
        curs.execute(_SQL)
        
