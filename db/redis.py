import redis
from redis import Redis

from configuration.config_file import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


async def get_redis_database() -> Redis:
    rd = redis.Redis(connection_pool=redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT,
                    password=REDIS_PASSWORD,decode_responses=True))

    return rd