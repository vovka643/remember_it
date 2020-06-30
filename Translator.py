from yandex_translate import YandexTranslate
import json
import numpy as np

class Translator:

    def __init__(self):
        yandex_token = 'trnsl.1.1.20160731T003337Z.2e4a2410132a1289.643df1d13471d33035d01a863f50536e71f8ef60'
        self.trans = YandexTranslate(yandex_token)
        
        with open('phrases.txt') as json_file:
            self.dictionary = json.load(json_file)

    def translate(self, phrase):
        return self.trans.translate(phrase, 'ru')['text'][0].rstrip()
    
    def get_phrase(self, word):
        
        if (word in set (self.dictionary.keys())):
            phrases = self.dictionary[word]
            phrase = phrases[np.random.randint(len(phrases))]
        else:
            phrase = word
            
        return phrase