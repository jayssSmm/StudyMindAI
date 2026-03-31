import redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_url=os.getenv('REDIS_URL')
database_url=os.getenv('DATABASE_URL')

redis_client = redis.Redis.from_url(
    redis_url,
    decode_responses=True
)