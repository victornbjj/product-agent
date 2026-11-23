import os
from dotenv import load_dotenv
from redis import Redis

load_dotenv()


client = Redis.from_url(os.getenv("REDIS_URL", ""))




