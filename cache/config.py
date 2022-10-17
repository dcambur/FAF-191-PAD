import os


class RedisConfig:
    expire = 18000  # 5 hours
    port = 6379
    host = os.environ["REDIS_HOST"]
