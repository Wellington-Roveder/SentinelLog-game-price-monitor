import redis
import os
from dotenv import load_dotenv

load_dotenv()


r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=3,
)
