import requests
from bs4 import BeautifulSoup
import re

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

    def get_lyrics(self):
        lyrics = ''
        for block in self.lyrics_blocks:
            lyrics = lyrics + '\n' + block.get_text('\n')
        return lyrics

    def get_word_list(self):
        words = list()
        for block in self.lyrics_blocks:
            words = words + re.findall('[’a-z$\'-]+', block.get_text('\n').lower())
        return words