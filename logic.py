import requests
from bs4 import BeautifulSoup
import re
import db
import os
import string
import datetime
from dateutil.relativedelta import relativedelta

import lyricsgenius as lg

api_key = str(os.environ.get('genius_token'))


def get_lyrics(name, author):
    genius = lg.Genius(api_key, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)
    genius.verbose = False
    genius.remove_section_headers = True
    song = genius.search_song(name, author)
    lyrics_dirty = song.lyrics
    index_to_cut = lyrics_dirty.find('Lyrics')
    lyrics = lyrics_dirty[index_to_cut + 6:-5].rstrip('0123456789')
    return lyrics

def get_word_list(name, author):
    return prettify_lyrics_to_list(get_lyrics(name, author))


# input is author + space + track name. if start default then Genius link otherwise simple uuid
def create_url(input, start='https://genius.com/'):
    url = start
    for word in input.capitalize().split(' '):
        url = url + word + '-'
    return url + 'lyrics'


def get_unknown_by_user(email, words_to_check):
    result = []
    if type(words_to_check) == 'str':
        words_to_check = words_to_check.split()
    known_words = db.get_words_by_user(email)
    known_english_words = [c[0] for c in known_words]
    for word in words_to_check:
        word = prettify_word(word)
        if not(word in known_english_words) and not(word in result):
            result.append(prettify_word(word))
    return result


def prettify_word(word):
    symbols = '!.,&?[]1234567890:;())@#%^*+=~…—"'
    for s in symbols:
        word = word.replace(s, '')
    result = word.replace('$', 's').lower().replace("`", "’").replace("'", "’")
    return result

def prettify_lyrics_to_list(lyrics):
    words = lyrics.split()
    new_words = []
    for word in words:
        new_words.append(prettify_word(word))
    return new_words


def get_age_by_date(register_date):
    current_date = datetime.datetime.now()
    time_difference = relativedelta(current_date, register_date)

    years = time_difference.years
    months = time_difference.months
    weeks = time_difference.weeks
    days = time_difference.days
    hours = time_difference.hours
    minutes = time_difference.minutes
    seconds = time_difference.seconds

    period_values = [years, months, weeks, days, hours, minutes, seconds]
    period_names = ['years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds']

    index = next(i for i, x in enumerate(period_values) if x != 0)
    time_string = f"{period_values[index]} {period_names[index]}"

    return time_string

def is_photo(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
