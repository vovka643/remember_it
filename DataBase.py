import pymongo
from User import User

class DataBase:
    
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client.jrdb   #database
        self.users_db = self.db.users  #collections for users
        
    def get_all_users(self):
        users = []
        for u in self.users_db.find():
            
            user = User()
            user.intervals = u['intervals']
            user.schedule  = u['schedule']
            user.next_word  = u['next_word']
            user.id  = u['id']
            user.history  = u['history']
            user.qflag  = u['qflag']
            user.correct_answer = u['correct_answer']
            user.current_answers = u['current_answers']
            
            users.append(user)
        
        return users
    
    def update(self, user):
        voc = {
            'intervals': user.intervals,
            'schedule':user.schedule,
            'next_word':user.next_word,
            'id':user.id,
            'history':user.history,
            'qflag':user.qflag,
            'correct_answer':user.correct_answer,
            'current_answers':user.current_answers
        }
        
        self.users_db.update_one({"id": user.id}, {"$set": voc}, upsert = True)
        