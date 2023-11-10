from random import randint

db = {}

def genera() -> str:
    return str(randint(1000000,9999999))

def get(key):
    return db.get(key,None)

def set(user_id):
    key = genera()
    db[key] = user_id
    return key