import os
import redis
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

database_url = os.getenv("DATABASE_URL")
redis_url = os.getenv("REDIS_URL")

redis_client = redis.Redis.from_url(
    redis_url,
    decode_responses=True
)