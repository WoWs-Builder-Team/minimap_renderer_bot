import redis
import aioredis
from utils.environ import check_environment_var

check_environment_var(["REDIS_URL"])


REDIS = redis.from_url("redis://:@localhost:6379/")
ASYNC_REDIS = aioredis.from_url("redis://:@localhost:6379/")
