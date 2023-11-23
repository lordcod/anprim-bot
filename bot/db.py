
poll_db = {}

def get(key):
    return poll_db.get(key)

def set(key,value):
    poll_db[key] = value