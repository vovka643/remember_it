import numpy as np
import datetime

class User:

    def __init__(self, id = 0):
        self.intervals = [10, 600, 18000, 86400, 432000, 2160000, 3153600000] # in seconds
        # self.intervals = [60, 60, 60, 60, 60, 3153600000] # in seconds
        self.schedule = [{'word':'Hello', 'next_time': 3153600000+self.get_now(), 'interval_number':-1,'pair_transl':'Hello', 'pair': 'Hello there'} ] # 3153600000 seconds in 100 years
        self.next_word = self.schedule[0]
        
        self.id = id
        self.history = {}
        self.qflag = False #question flag
        self.correct_answer = -1
        self.current_answers = []

        
    def process_word (self, message_text, translator, bot): # change name of function
        
        bot.send_message(self.id, message_text + ' - ' + translator.translate(message_text))
        #todo if message text in one word
        word = message_text
        #get pair
        pair = translator.get_phrase(message_text)
        pair_transl = translator.translate(pair)
        bot.send_message(self.id, pair + ' - ' + pair_transl)

        self.add_to_history(word, pair, pair_transl)
        self.add_to_schedule(word, pair, pair_transl)
    
        pass
        
    def answer(self, message_text, translator, bot):  # change name of function
        
        # пусть сюда прлетает сообщения, которые только для пользоветля, без служебных
        
        if self.qflag:
            if (message_text in set(self.current_answers)):
                #check it with correct answer
                if (message_text == self.current_answers[self.correct_answer]):
                    bot.send_message(self.id, 'Correct!')
                    self.change_current_interval(1)
                    
                else:
                    bot.send_message(self.id, self.next_word['pair'] + ' - ' + self.next_word['pair_transl'])
                    self.change_current_interval(-1)
                    
                self.qflag = False
                self.set_next_word()
                
            else:
                self.process_word(message_text, translator, bot)
                self.send_question(bot)
                
        else:
            self.process_word(message_text, translator, bot)
            
            
    def send_question(self, bot):
        
        random_pairs = self.get_random_pairs()
        answers = [rp[2] for rp in random_pairs]
        self.qflag = True
        self.increase_word_interval()
        
        self.correct_answer = np.random.randint(3)
        answers.insert(self.correct_answer, self.next_word['pair_transl'])
        self.current_answers = answers
        
        bot.send_message(self.id, self.next_word['pair'], answers)
        

    def get_random_pairs(self):
        result = []
        if len(self.history) > 3:
            words = list(self.history.keys())
            for i in range(3):
                result.append(self.history[words[np.random.randint(len(self.history))]][0])
        else:
            result = [(0, 'green house', 'зеленый дом'),
                      (0, 'white snow', 'белый снег'),
                      (0, 'long snake', 'длинная змея')]
        return result
    
    def add_to_history(self, word, pair, pair_transl): 
        now = self.get_now()
        if word in self.history.keys():
            self.history[word].append((now, pair, pair_transl))
        else:
            self.history[word] = [(now, pair, pair_transl)]

    def change_current_interval(self, upper):
        interval_number = self.next_word['interval_number']
        self.intervals[interval_number] = self.intervals[interval_number]*(1+upper*0.05)

    def set_next_word(self):
        next_word = self.schedule[0]
        for word in self.schedule:
            if (next_word['next_time'] > word['next_time']):
                next_word = word
        self.next_word = next_word

    def add_to_schedule(self, word, pair, pair_transl):
        self.schedule.append({'word':word, 'pair':pair, 'pair_transl':pair_transl, 'interval_number':0, 'next_time': self.get_now()+self.intervals[0]})
        self.set_next_word()

    def increase_word_interval(self):
        if (self.next_word['interval_number'] < len(self.intervals)-1):
            self.next_word['interval_number'] += 1
            self.next_word['next_time'] = self.get_now() + self.intervals[self.next_word['interval_number']]
            #self.set_current_word()
        else:
            #self.schedule.remove(self.next_word)
            pass

    def get_now(self):
        return round((datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds())
