import redis
import aioredis
from os import environ
from utils.environ import check_environment_var

check_environment_var(
    ["REDIS_HOST", "REDIS_PORT", "REDIS_USERNAME", "REDIS_PASSWORD"]
)

REDIS = redis.StrictRedis(
    host=environ.get("REDIS_HOST", "localhost"),
    port=int(environ.get("REDIS_PORT", 6379)),
    username=environ.get("REDIS_USERNAME"),
    password=environ.get("REDIS_PASSWORD"),
)

ASYNC_REDIS = aioredis.StrictRedis(
    host=environ.get("REDIS_HOST", "localhost"),
    port=int(environ.get("REDIS_PORT", 6379)),
    username=environ.get("REDIS_USERNAME"),
    password=environ.get("REDIS_PASSWORD"),
)
