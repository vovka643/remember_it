from MyBot import MyBot
from Translator import Translator
from User import User
from DataBase import DataBase
import const

import datetime
import traceback
import pymongo

def get_user(users, id):
    #find user
    for usr in users:
        if usr.id == id:
            return usr
    #create new user
    user = User(id)
    users.append(user)
    return user

def help_handler(user_id, bot):
    text = 'Этот бот помогает запоминать английские слова, продбирая к ним словосочетание и повторяя их тебе. Просто введи незнакомое английское слово, остальное сделает этот бот. Переводчик - yandex translator'
    bot.send_message(user_id, text)
    
translator = Translator()

bot_token = const.bot_token #justReadBooktmp2_bot
bot = MyBot(bot_token)

#add Data Base
db = DataBase()

#full list of users from data base
users = db.get_all_users()
    
upd_offset = 0

special_i = 0
while special_i < 5:
    special_i = special_i + 1
    
    try:
        updates = bot.get_updates(offset=upd_offset)

        while (len(updates)==0):
            updates = bot.get_updates(offset=upd_offset)

        update = updates[-1]
        last_message_id = update.message.message_id
        upd_offset = update.update_id - 1

        #my fucking dispatcher with black jack and whores
        while True:
            updates = bot.get_updates(offset=upd_offset)

            i = -1
            if (len(updates)>0):
                mes_id = updates[i].message.message_id
                if updates[i].message:
                    while ((mes_id != last_message_id) and (-i <= len(updates))):

                        user_id = updates[i].message.from_user.id
                        user = get_user(users, user_id)
                        mes = updates[i].message.text

                        if (mes == '/help'):
                            help_handler(user.id, bot)
                        else:
                            user.answer(mes, translator, bot)
                            #todo: logging
                            db.update(user)

                        i = i-1
                        if (-i <= len(updates)):
                            mes_id = updates[i].message.message_id

                    last_message_id = updates[-1].message.message_id
                    upd_offset = updates[-1].update_id - 1

            now = round((datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds())
            for us in users:
                if now >= us.next_word['next_time'] and (not us.qflag) :

                    us.send_question(bot)
                    
                    #todo: logging
                    db.update(user)

    except Exception as e:
        file = open('error.log','w')
        file.write('FATAL ERROR\n')
#         file.write(date_str())
        file.write(traceback.format_exc())
        #print(traceback.format_exc())
        file.write('end of error')
        file.close()            