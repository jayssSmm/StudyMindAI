import redis

r = redis.Redis(
    host="localhost",
    port=7379,
    decode_responses=True
)

