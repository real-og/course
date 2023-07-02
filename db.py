import os
import psycopg2
from psycopg2.extras import DictCursor
from deep_translator import GoogleTranslator
import logic


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
        word = logic.prettify_word(word)
        trans = translator.translate(word) 
        _SQL = f"INSERT INTO words (word, translate) VALUES ('{word}', '{trans}');"
        curs.execute(_SQL)
        return True

def check_word(word):
    word = logic.prettify_word(word)
    with Database() as curs:
        _SQL = f"SELECT word FROM words WHERE word = '{word}';"
        curs.execute(_SQL)
        if len(curs.fetchall()) == 0:
            return False
        return True

def add_word_to_user(email, word):
    with Database() as curs:
        word = logic.prettify_word(word)
        if check_word_by_user(email, word):
            return
        if not check_word(word):
            add_word(word)
        _SQL = f"""insert into user_word (iduser, idword)
                    select users.id, words.id
                    from users inner join words on
                    words.word = '{word}' and users.email = '{email}';"""
        curs.execute(_SQL)


def add_full_lyrics(email, lyrics):
    words = logic.prettify_lyrics_to_list(lyrics)
    with Database() as curs:
        _SQL = f"""insert into words (word, translate) values """
        for word in words:
            _SQL += f"('{word}', 'mock'), "
        
        _SQL = _SQL[:-2] + " ON CONFLICT (word) DO NOTHING;"
        curs.execute(_SQL)
        _SQL = f"""WITH user_id_cte AS (
                   SELECT id FROM users WHERE email = '{email}'
                   )
                   INSERT INTO user_word (iduser, idword)
                   SELECT user_id_cte.id, words.id  
                   FROM user_id_cte, words  
                   WHERE words.word IN ("""
        for word in words:
            _SQL += f"'{word}', "
        _SQL = _SQL[:-2] + ") on conflict do nothing;"
        curs.execute(_SQL)
                 

def delete_word_from_user(email, word):
    with Database() as curs:
        word = logic.prettify_word(word)
        _SQL = f"""delete from user_word
                   where idword = (select id from words where word='{word}')
                   and iduser = (select id from users where email='{email}');"""
        curs.execute(_SQL)

def add_song_to_user(email, name, author):
    with Database() as curs:
        if check_song_by_user(email, name, author):
            return
        if not check_song(name, author):
            add_song(name, author)
        _SQL = f"""insert into song_user (iduser, idsong)
                    select users.id, songs.id
                    from users inner join songs on
                    songs.name = '{name}' and users.email = '{email}' and songs.author = '{author}';"""
        curs.execute(_SQL)

def add_song(name, author):
    if check_song(name, author):
        return False
    with Database() as curs: 
        _SQL = f"INSERT INTO songs (name, author) VALUES ('{name}', '{author}');"
        curs.execute(_SQL)
        return True

def check_song(name, author):
    with Database() as curs:
        _SQL = f"SELECT * FROM songs WHERE name = '{name}' and author = '{author}';"
        curs.execute(_SQL)
        if len(curs.fetchall()) == 0:
            return False
        return True

def check_song_by_user(email, name, author):
    with Database() as curs:
        _SQL = f"""select * from song_user where 
                    iduser = (select id from users where email = '{email}')
                    and idsong = (select id from songs where name = '{name}' and author = '{author}');"""
        curs.execute(_SQL)
        if len(curs.fetchall()) == 0:
            return False
        return True

def check_word_by_user(email, word):
    with Database() as curs:
        word = logic.prettify_word(word)
        _SQL = f"""select * from user_word where 
                    iduser = (select id from users where email = '{email}')
                    and idword = (select id from words where word = '{word}');"""
        curs.execute(_SQL)
        if len(curs.fetchall()) == 0:
            return False
        return True

def delete_word_by_user(email, word):
    with Database() as curs:
        word = logic.prettify_word(word)
        _SQL = f"""delete from user_word where
                    iduser = (select id from users where email = '{email}')
                    and idword = (select id from words where word = '{word}');"""
        curs.execute(_SQL)

def get_word_count_by_user(email):
    with Database() as curs:
        _SQL = f"""select count(*)
                    from user_word inner join words
                    on user_word.iduser = (select id from users where email = '{email}')
                    and user_word.idword = words.id;"""
        curs.execute(_SQL)
        return curs.fetchone()[0]

def get_song_count_by_user(email):
    with Database() as curs:
        _SQL = f"""select count(*)
                    from song_user inner join songs
                    on song_user.iduser = (select id from users where email = '{email}')
                    and song_user.idsong = songs.id;"""
        curs.execute(_SQL)
        return curs.fetchone()[0]

def get_words_by_user(email) -> list(()):
    with Database() as curs:
        _SQL = f"""select word, translate
                    from user_word inner join words
                    on user_word.iduser = (select id from users where email = '{email}')
                    and user_word.idword = words.id order by word;"""
        curs.execute(_SQL)
        res = curs.fetchall()
        return [(tupl['word'], tupl['translate']) for tupl in res]
        

def get_top_by_words():
    with Database() as curs:
        _SQL =f"""select name, count  
                  from users inner join 
                  (select  email, count(email) as count 
                  from users inner join user_word on users.id = user_word.iduser 
                  group by email order by count(email)) as e on users.email=e.email order by count desc limit 20;"""
        curs.execute(_SQL)
        return curs.fetchall()

def get_songs_by_artists(artists):
    with Database() as curs:
        _SQL =f"select * from songs where author IN ("
        for artist in artists:
            _SQL += f"'{artist}', "
        curs.execute(_SQL[:-2] + ');')
        return curs.fetchall()
    
def change_photo_by_user(email, photo):
    with Database() as curs:
        _SQL = f"UPDATE users SET photo = {psycopg2.Binary(photo)} WHERE email = '{email}';"
        curs.execute(_SQL)


def get_photo_by_user(email):
    with Database() as curs:
        _SQL =f"select photo from users where email = '{email}'"
        curs.execute(_SQL)
        return curs.fetchone()['photo']



        
