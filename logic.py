import requests
from bs4 import BeautifulSoup
import re
import db

# input is author + space + track name. if start default then Genius link otherwise simple uuid
def create_url(input, start='https://genius.com/'):
    url = start
    for word in input.capitalize().split(' '):
        url = url + word + '-'
    return url + 'lyrics'

class LyricsParser:
    def __init__(self, url):
        self.url = url
        try:
            self.page = requests.get(url)
            self.soup = BeautifulSoup(self.page.text, "html.parser")
        except Exception as e:
            print(e)
            self.page = 'bam'
            self.soup = BeautifulSoup('bang', "html.parser")
        self.lyrics_blocks = self.soup.findAll(class_="Lyrics__Container-sc-1ynbvzw-6 YYrds") 

    def get_lyrics(self) -> str:
        lyrics = ''
        for block in self.lyrics_blocks:
            lyrics = lyrics + '\n' + block.get_text('\n')
        return lyrics

    def get_word_list(self):
        words = list()
        for block in self.lyrics_blocks:
            words = words + re.findall('[’a-z$\'-]+', block.get_text('\n').lower())
        return words

def get_unknown_by_user(email, words):
    result = []
    if type(words) == 'str':
        words = words.split()
    known = db.get_words_by_user(email)
    known_english_words = [c[0] for c in known]
    for word in words:
        word = prettify_word(word)
        if not(word in known_english_words) and not(word in result):
            result.append(prettify_word(word))
    return result

def prettify_word(word):
    symbols = '!.,&?[]1234567890:;())@#%^*+=~…—'
    for s  in symbols:
        word = word.replace(s, '')
    return word.replace('$', 's').lower().replace("`", "’").replace("'", "’")