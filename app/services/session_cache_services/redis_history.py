from app.extensions import redis_client as r

HISTORY_TTL = 60 * 60 * 24  # 24 hours

def set_history(session_id,message_id,role,message):

    key = f'session_id:{session_id}'
    r.hset(message_id,mapping={'role':role,'content':message})

    r.rpush(key,)
    r.expire('chat_history_groq', HISTORY_TTL)

    return True
    

def get_last_ten_messages(session_id,n:int=10):
    return list(filter(lambda x:r.hgetall(f'session_id:{session_id}'), r.lrange("chat_history_groq",-n,-1)))