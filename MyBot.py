import telebot

class MyBot:
    
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
    
    def send_message(self, user_id, message, answers = None):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False, row_width=1)
        
        if (answers != None):
            for i in range(len(answers) // 2):
                user_markup.row(answers[i*2],answers[i*2 + 1] )
            if (len(answers) % 2 > 0):
                user_markup.add(answers[-1])
        else:
            user_markup = telebot.types.ReplyKeyboardRemove() # hideBoard   
        self.bot.send_message(user_id, message, reply_markup=user_markup)
        
    def get_updates(self, offset = -1):
        updates = []
        try: 
            updates = self.bot.get_updates(offset=offset)
        except Exception as e:
            file = open('error.log','w')
            file.write('error in MyBot.get_updates\n')
    #         file.write(date_str())
            file.write(traceback.format_exc())
            file.write('end of error')
            file.close()     
        
        return updates