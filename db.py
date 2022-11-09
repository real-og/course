import psycopg2
import os
from psycopg2.extras import DictCursor
from deep_translator import GoogleTranslator


translator = GoogleTranslator(source='en', target='ru')

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

def add_word(word):
    if check_word(word):
        return False
    with Database() as curs:
        word = word.replace("`", "’").replace("'", "’")
        trans = translator.translate(word) 
        _SQL = f"INSERT INTO words (word, translate) VALUES ('{word}', '{trans}');"
        curs.execute(_SQL)
        return True

def check_word(word):
    word = word.replace("`", "’").replace("'", "’")
    with Database() as curs:
        _SQL = f"SELECT word FROM words WHERE word = '{word}';"
        curs.execute(_SQL)
        if len(curs.fetchall()) == 0:
            return False
        return True

def add_word_to_user(email, word):
    with Database() as curs:
        word = word.replace("`", "’").replace("'", "’")
        if not check_word(word):
            add_word(word)
        _SQL = f"""insert into user_word (iduser, idword)
                    select users.id, words.id
                    from users inner join words on
                    words.word = '{word}' and users.email = '{email}';"""
        curs.execute(_SQL)

def check_word_by_user(email, word):
    with Database() as curs:
        word = word.replace("`", "’").replace("'", "’")
        _SQL = f"""select * from user_word where 
                    iduser = (select id from users where email = '{email}')
                    and idword = (select id from words where word = '{word}');"""
        curs.execute(_SQL)
        if len(curs.fetchall()) == 0:
            return False
        return True

def delete_word_by_user(email, word):
    with Database() as curs:
        word = word.replace("`", "’").replace("'", "’")
        _SQL = f"""delete from user_word where
                    iduser = (select id from users where email = '{email}')
                    and idword = (select id from words where word = '{word}');"""
        curs.execute(_SQL)

def get_words_by_user(email):
    with Database() as curs:
        _SQL = f"""select word, translate
                    from user_word inner join words
                    on user_word.iduser = (select id from users where email = '{email}')
                    and user_word.idword = words.id order by word;"""
        curs.execute(_SQL)
        res = curs.fetchall()

        return [(tupl[0], tupl[1]) for tupl in res]
        #return curs.fetchall()

def get_top_by_words():
    with Database() as curs:
        _SQL =f"""select  email, count(email)
                  from users inner join user_word
                  on users.id = user_word.iduser
                  group by email order by count(email) desc limit 20;"""
        curs.execute(_SQL)
        return curs.fetchall()

        
