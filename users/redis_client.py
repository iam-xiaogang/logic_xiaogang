# author xiaogang
import redis
from django.conf import settings

pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True  # 自动解码成 str
)

redis_client = redis.StrictRedis(connection_pool=pool)
